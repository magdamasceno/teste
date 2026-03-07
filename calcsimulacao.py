import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Relatório RA Oficial", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Relatório RA - Ajuste de Precisão")

with st.sidebar:
    st.header("⚙️ Painel Geral")
    total_reclamacoes = st.number_input("Total de Reclamações", value=12774)
    total_respostas = st.number_input("Total de Respostas", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0

if "dados_brutos" not in st.session_state:
    st.session_state.dados_brutos = pd.DataFrame({
        "Mês": ["OUTUBRO", "NOVEMBER", "DEZEMBRO", "JANEIRO", "FEVEREIRO", "MARÇO"],
        "Nota": [7.38, 7.42, 7.44, 7.25, 7.72, 8.00],
        "Avaliações": [1086, 1542, 1129, 1144, 711, 68],
        "Resolvidos": [952, 1342, 981, 992, 619, 61],
        "Voltariam": [899, 1277, 930, 917, 590, 57]
    })

df_digitacao = st.data_editor(st.session_state.dados_brutos, use_container_width=True)

if st.button("🚀 GERAR RELATÓRIO FINAL", use_container_width=True):
    # Cópia para cálculos
    df_calc = df_digitacao.copy()
    
    # FORÇANDO O CÁLCULO EXATO (Igual ao seu manual)
    # Usamos round(x, 3) para garantir que a porcentagem fique com 1 casa decimal precisa
    df_calc["% Solução"] = (df_calc["Resolvidos"] / df_calc["Avaliações"] * 100).round(1)
    df_calc["% Voltaria"] = (df_calc["Voltariam"] / df_calc["Avaliações"] * 100).round(1)

    st.subheader("📋 Relatório Mensal Calculado")
    st.dataframe(df_calc, use_container_width=True)

    # CÁLCULOS TOTAIS (PONDERADOS)
    total_av = df_calc["Avaliações"].sum()
    
    # Nota Ponderada
    mn_ponderada = (df_calc["Nota"] * df_calc["Avaliações"]).sum() / total_av
    
    # Índices Brutos (Soma total / Avaliações totais)
    is_total = (df_calc["Resolvidos"].sum() / total_av) * 100
    inn_total = (df_calc["Voltariam"].sum() / total_av) * 100

    # AR FINAL
    ar_final = ((ir_geral * 2) + (mn_ponderada * 10 * 3) + (is_total * 3) + (inn_total * 2)) / 100

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nota (MN)", f"{mn_ponderada:.2f}")
    c2.metric("Solução (IS)", f"{is_total:.1f}%")
    c3.metric("Voltaria (INN)", f"{inn_total:.1f}%")
    c4.metric("SCORE (AR)", f"{ar_final:.2f}")
