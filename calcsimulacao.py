import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Calculadora RA - Final", layout="wide")

# Estilo Visual para o Tema Escuro
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora RA - MAGDA")

# Sidebar com valores fixos para bater o Score Final
with st.sidebar:
    st.header("⚙️ Painel Geral")
    total_reclamacoes = st.number_input("Total Reclamações", value=12774)
    total_respostas = st.number_input("Total Respondidas", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta: {ir_geral:.1f}%")

st.subheader("1️⃣ Conferência de Dados Brutos")

opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# Carregamento automático dos dados das imagens
if "dados_automaticos" not in st.session_state:
    st.session_state.dados_automaticos = pd.DataFrame({
        "Mês": ["OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO", "MARÇO"],
        "Nota Consumidor": [7.38, 7.42, 7.44, 7.25, 7.72, 8.00],
        "Avaliações": [1086, 1542, 1129, 1144, 711, 68],
        "Resolvidos": [952, 1342, 981, 992, 619, 61],
        "Voltariam": [899, 1277, 930, 917, 590, 57]
    })

# Editor com Lista Suspensa
df_input = st.data_editor(
    st.session_state.dados_automaticos,
    num_rows="fixed",
    use_container_width=True,
    key="editor_fiel_v5",
    column_config={
        "Mês": st.column_config.SelectboxColumn("Mês", options=opcoes_meses),
        "Nota Consumidor": st.column_config.NumberColumn(format="%.2f"),
    }
)

st.markdown("---")

if st.button("🚀 GERAR RELATÓRIO E CALCULAR AR", use_container_width=True):
    
    df_calc = df_input.copy()
    
    # Lógica para truncar (Ex: 87,66% vira 87,6%) para bater com seu manual
    df_calc["% Solução"] = np.floor((df_calc["Resolvidos"] / df_calc["Avaliações"] * 1000)) / 10
    df_calc["% Voltaria"] = np.floor((df_calc["Voltariam"] / df_calc["Avaliações"] * 1000)) / 10

    st.subheader("2️⃣ Relatório de Performance Mensal")
    
    # Exibição corrigida do DataFrame
    st.dataframe(
        df_calc.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%",
            "Nota Consumidor": "{:.2f}"
        }), 
        use_container_width=True
    )

    # CÁLCULOS TOTAIS (Média Ponderada e Soma Bruta)
    total_av = df_calc["Avaliações"].sum()
    total_res = df_calc["Resolvidos"].sum()
    total_vol = df_calc["Voltariam"].sum()

    # Índices Globais (Soma Bruta / Soma Bruta)
    is_global = (total_res / total_av) * 100 if total_av > 0 else 0
    inn_global = (total_vol / total_av) * 100 if total_av > 0 else 0
    
    # Nota Ponderada (MN)
    mn_ponderada = (df_calc["Nota Consumidor"] * df_calc["Avaliações"]).sum() / total_av if total_av > 0 else 0

    # AR Final
    ar_final = ((ir_geral * 2) + (mn_ponderada * 10 * 3) + (is_global * 3) + (inn_global * 2)) / 100

    st.divider()
    st.subheader(f"3️⃣ Resultado Final Consolidado: AR {ar_final:.2f}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nota (MN)", f"{mn_ponderada:.2f}")
    col2.metric("Solução (IS)", f"{is_global:.1f}%")
    col3.metric("Voltaria (INN)", f"{inn_global:.1f}%")
    col4.metric("SCORE (AR)", f"{ar_final:.2f}")
