import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Médias 6 Meses", layout="wide")

# Estilo para parecer uma planilha limpa
st.markdown("""
    <style>
        .stApp { background-color: #f4f7f6; }
        h1, h2, h3 { color: #2c3e50 !important; }
        .stDataFrame { border: 1px solid #dcdde1; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Média (Últimos 6 Meses)")
st.write("Insira os dados brutos de cada mês para calcular as porcentagens e médias automáticas.")

# 1. CRIAR TABELA EM BRANCO (6 linhas para 6 meses)
# As colunas são baseadas na sua foto do Excel
colunas = ["Mês", "Nota Consumidor", "Total Avaliações", "Total Solução", "Total Voltaria"]
df_vazio = pd.DataFrame([{"Mês": "", "Nota Consumidor": 0.0, "Total Avaliações": 0, "Total Solução": 0, "Total Voltaria": 0} for _ in range(6)])

# 2. EDITOR DE TABELA (ESTILO EXCEL)
st.subheader("📝 Preenchimento de Dados")
df_editado = st.data_editor(
    df_vazio,
    use_container_width=True,
    num_rows="fixed", # Trava em 6 meses
    key="planilha_6_meses",
    column_config={
        "Mês": st.column_config.TextColumn("Mês (Ex: Jan, Fev...)"),
        "Nota Consumidor": st.column_config.NumberColumn("Nota Consumidor", format="%.2f"),
        "Total Avaliações": st.column_config.NumberColumn("Qtd. Avaliações"),
        "Total Solução": st.column_config.NumberColumn("Qtd. Soluções"),
        "Total Voltaria": st.column_config.NumberColumn("Qtd. Voltariam")
    }
)

# 3. CÁLCULOS AUTOMÁTICOS (ESTILO EXCEL)
if df_editado["Total Avaliações"].sum() > 0:
    # Calculando as porcentagens individuais de cada linha (Mês)
    df_calculado = df_editado.copy()
    
    # Evita divisão por zero
    mask = df_calculado["Total Avaliações"] > 0
    df_calculado["% Solução"] = 0.0
    df_calculado["% Voltaria"] = 0.0
    
    df_calculado.loc[mask, "% Solução"] = (df_calculado["Total Solução"] / df_calculado["Total Avaliações"]) * 100
    df_calculado.loc[mask, "% Voltaria"] = (df_calculado["Total Voltaria"] / df_calculado["Total Avaliações"]) * 100

    # 4. EXIBIÇÃO DOS RESULTADOS POR MÊS
    st.divider()
    st.subheader("📈 Resultado Processado")
    
    # Formatação para exibição
    st.dataframe(
        df_calculado.style.format({
            "Nota Consumidor": "{:.2f}",
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%"
        }),
        use_container_width=True
    )

    # 5. MÉDIA FINAL DOS 6 MESES
    total_av = df_calculado["Total Avaliações"].sum()
    total_sol = df_calculado["Total Solução"].sum()
    total_vol = df_calculado["Total Voltaria"].sum()
    
    # Média ponderada da nota (Nota * Avaliações / Total Avaliações)
    media_nota = (df_calculado["Nota Consumidor"] * df_calculado["Total Avaliações"]).sum() / total_av
    perc_sol_geral = (total_sol / total_av) * 100
    perc_vol_geral = (total_vol / total_av) * 100

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Média das Notas (6m)", f"{media_nota:.2f}")
    col2.metric("% Solução Geral (6m)", f"{perc_sol_geral:.1f}%")
    col3.metric("% Voltaria Geral (6m)", f"{perc_vol_geral:.1f}%")

else:
    st.warning("Aguardando o preenchimento dos dados para calcular as médias.")
