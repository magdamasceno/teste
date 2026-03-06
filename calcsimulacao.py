import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Calculadora RA - Pro", layout="wide")

# Estilo personalizado para parecer um Dashboard
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3 { color: #3cba54 !important; }
        .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Performance RA (Mensal)")

# --- CONFIGURAÇÃO INICIAL (FORA DA TABELA) ---
with st.sidebar:
    st.header("⚙️ Dados Fixos do Período")
    total_reclamacoes = st.number_input("Total Reclamações (Geral)", value=12774)
    total_respostas = st.number_input("Total Respostas (Geral)", value=12509)

# --- TABELA ESTILO EXCEL ---
st.subheader("📝 Preencha os dados dos meses")
st.info("Dica: Clique nas células para editar e no '+' para adicionar novos meses.")

# Criando a estrutura base (Exemplo com os dados da sua foto)
dados_iniciais = [
    {"Mês": "Setembro", "Nota Consumidor": 7.3, "Resolvidos": 938, "Voltariam": 880, "Avaliações": 1116},
    {"Mês": "Outubro", "Nota Consumidor": 7.37, "Resolvidos": 944, "Voltariam": 891, "Avaliações": 1078},
    {"Mês": "Novembro", "Nota Consumidor": 7.42, "Resolvidos": 1324, "Voltariam": 1260, "Avaliações": 1526},
]

df_editor = st.data_editor(
    pd.DataFrame(dados_iniciais),
    num_rows="dynamic",
    column_config={
        "Mês": st.column_config.TextColumn("Mês", required=True),
        "Nota Consumidor": st.column_config.NumberColumn("Nota (0-10)", min_value=0.0, max_value=10.0, format="%.2f"),
        "Resolvidos": st.column_config.NumberColumn("Qtd Resolvidos", min_value=0),
        "Voltariam": st.column_config.NumberColumn("Qtd Voltariam", min_value=0),
        "Avaliações": st.column_config.NumberColumn("Total Avaliações", min_value=1),
    },
    use_container_width=True,
    key="editor_mensal"
)

# --- LÓGICA DE CÁLCULO ---
if not df_editor.empty:
    # Totais Acumulados
    total_av = df_editor["Avaliações"].sum()
    total_res = df_editor["Resolvidos"].sum()
    total_vol = df_editor["Voltariam"].sum()
    
    # Médias Ponderadas (Calculando a porcentagem automaticamente como você pediu)
    # Média das Notas (Média Ponderada pelo número de avaliações de cada mês)
    mn_final = (df_editor["Nota Consumidor"] * df_editor["Avaliações"]).sum() / total_av
    
    # Índices em %
    is_final = (total_res / total_av) * 100
    inn_final = (total_vol / total_av) * 100
    ir_final = (total_respostas / total_reclamacoes) * 100

    # Fórmula AR Oficial
    # AR = ((IR*2) + (MN*10*3) + (IS*3) + (INN*2)) / 100
    ar_score = ((ir_final * 2) + (mn_final * 10 * 3) + (is_final * 3) + (inn_final * 2)) / 100

    # --- EXIBIÇÃO DO RESULTADO ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Média das Notas (MN)", f"{mn_final:.2f}")
    c2.metric("Índice Solução (IS)", f"{is_final:.1f}%")
    c3.metric("Novos Negócios (INN)", f"{inn_final:.1f}%")
    c4.metric("NOTA FINAL (AR)", f"{ar_score:.2f}", delta=f"{ar_score-8.0:.2f}" if ar_score > 8 else None)

    # Dica de Reputação
    if ar_score >= 8: st.success("🏆 Reputação Estimada: **RA1000**")
    elif ar_score >= 7: st.info("🟢 Reputação Estimada: **ÓTIMO**")
    else: st.warning("🟡 Reputação Estimada: **BOM / REGULAR**")
