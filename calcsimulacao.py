import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Relatório RA - Dados Carregados", layout="wide")

# Estilo Visual
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora RA - Dados Automáticos")

# Sidebar - Configurações fixas do seu painel
with st.sidebar:
    st.header("⚙️ Painel Geral (Fixo)")
    total_reclamacoes = st.number_input("Total Reclamações", value=12774)
    total_respostas = st.number_input("Total Respondidas", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta: {ir_geral:.1f}%")

st.subheader("1️⃣ Conferência de Dados (Já preenchidos)")

# Opções para a lista suspensa
opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# DADOS DA SUA IMAGEM (Carregados automaticamente para você não cansar de digitar)
if "dados_preenchidos" not in st.session_state:
    st.session_state.dados_preenchidos = pd.DataFrame({
        "Mês": ["OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO", "MARÇO"],
        "Nota Consumidor": [7.38, 7.42, 7.44, 7.25, 7.72, 8.00],
        "Avaliações": [1086, 1542, 1129, 1144, 711, 68],
        "Resolvidos": [952, 1342, 981, 992, 619, 61],
        "Voltariam": [899, 1277, 930, 917, 590, 57]
    })

# Editor de Dados com Lista Suspensa (Você ainda pode alterar se quiser)
df_input = st.data_editor(
    st.session_state.dados_preenchidos,
    num_rows="fixed",
    use_container_width=True,
    key="editor_final_auto",
    column_config={
        "Mês": st.column_config.SelectboxColumn("Mês", options=opcoes_meses),
        "Nota Consumidor": st.column_config.NumberColumn(format="%.2f"),
    }
)

st.markdown("---")

# Botão para processar o relatório
if st.button("🚀 GERAR RELATÓRIO E CALCULAR AR", use_container_width=True):
    
    df_calc = df_input.copy()
    
    # Lógica de arredondamento para baixo (Truncar) para bater o 87,6% em Outubro
    # Multiplicamos por 1000, pegamos o inteiro (floor) e dividimos por 10
    df_calc["% Solução"] = np.floor((df_calc["Resolvidos"] / df_calc["Avaliações"] * 1000)) / 10
    df_calc["% Voltaria"] = np.floor((df_calc["Voltariam"] / df_calc["Avaliações"] * 1000)) / 10

    # 1. EXIBIÇÃO DO RELATÓRIO MENSAL
    st.subheader("2️⃣ Performance Mensal Detalhada")
    st.dataframe(df_calc.style.format({
        "% Solução": "{:.1f}%",
        "% Voltaria": "{:.1f}%",
        "Nota Consumidor": "{:.2f}"
    }), use_container_width=True
