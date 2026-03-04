# --- PASSO 1: FERRAMENTAS ---
import pandas as pd
import os

# --- PASSO 2: CAMINHO DO ARQUIVO ---
caminho = '/content/sample_data/GOLLOG 6.xlsx'

if not os.path.exists(caminho):
    print("❌ Arquivo 'GOLLOG 6.xlsx' não encontrado!")
else:
    # --- PASSO 3: LEITURA E LIMPEZA TOTAL ---
    df = pd.read_excel(caminho)
    
    # Limpa os títulos das colunas (tira espaços e deixa em maiúsculo)
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Usa a Coluna I (índice 8) para a data
    col_data = df.columns[8]
    df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
    df = df.dropna(subset=[col_data])
    
    # --- PASSO 4: FILTRO DE MODERAÇÃO ---
    # Só faz o cálculo se a coluna MODERAÇÃO existir
    if 'MODERAÇÃO' in df.columns:
        df_calc = df[~df['MODERAÇÃO'].astype(str).str.contains('ACEITA|DESATIVADA', na=False, case=False)].copy()
    else:
        df_calc = df.copy()

    # --- PASSO 5: PREPARAÇÃO DOS MESES (EVITA ERROS DE REPETIÇÃO) ---
    # Remove colunas de cálculos anteriores para não dar 'already exists'
    for c in ['MES_RELATORIO', 'ORDEM_MES']:
        if c in df_calc.columns:
            df_calc = df_calc.drop(columns=[c])

    df_calc['MES_RELATORIO'] = df_calc[col_data].dt.strftime('%m/%Y')
    df_calc['ORDEM_MES'] = df_calc[col_data].dt.strftime('%Y%m')

    # --- PASSO 6: FUNÇÃO DE CÁLCULO (AJUSTADA PARA "SIM" / "NÃO") ---
    def calcular_gollog(x):
        total = len(x)
        # Na sua foto, o índice de solução usa "SIM" ou "NÃO"
        sol = len(x[x['ÍNDICE DE SOLUÇÃO'].astype(str).str.upper() == 'SIM'])
        vol = len(x[x['VOLTARIA A FAZER NEGÓCIO'].astype(str).str.upper() == 'SIM'])
        
        return pd.Series({
            'NOTA MÉDIA': round(x['NOTA'].mean(), 2),
            'SOLUÇÃO (%)': f"{(sol/total*100):.1f}%",
            'FIDELIDADE (%)': f"{(vol/total*100):.1f}%",
            'VOL. RECLAMAÇÕES': total
        })

    # --- PASSO 7: RELATÓRIO FINAL ---
    relatorio = df_calc.groupby(['ORDEM_MES', 'MES_RELATORIO']).apply(calcular_gollog).reset_index()
    
    # Pega os 6 meses mais recentes
    resultado = relatorio.sort_values('ORDEM_MES', ascending=False).head(6)
    resultado = resultado.drop(columns=['ORDEM_MES']).set_index('MES_RELATORIO')

    print("📊 RESULTADO CONSOLIDADO - ÚLTIMOS 6 MESES")
    print("=" * 65)
    print(resultado)
    print("=" * 65)
