import streamlit as st
import pandas as pd

st.set_page_config(page_title="Relatório RA Final", layout="wide")

# Estilo visual
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Relatório RA - Lógica de Acumulado")

# Sidebar
with st.sidebar:
    st.header("⚙️ Painel Geral")
    total_reclamacoes = st.number_input("Total de Reclamações (Painel)", value=12774)
    total_respostas = st.number_input("Total de Respostas (Painel)", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta: {ir_geral:.1f}%")

st.subheader("1️⃣ Inserção de Dados Mensais")

if "dados_brutos" not in st.session_state:
    st.session_state.dados_brutos = pd.DataFrame({
        "Mês": ["SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO"],
        "Nota": [7.27, 7.37, 7.42, 7.44, 7.25, 7.72],
        "Avaliações": [1129, 1083, 1542, 1120, 1144, 711],
        "Resolvidos": [946, 952, 1342, 961, 992, 619],
        "Voltariam": [889, 899, 1277, 922, 917, 590]
    })

df_digitacao = st.data_editor(
    st.session_state.dados_brutos,
    num_rows="fixed",
    use_container_width=True,
    key="editor_final_v3"
)

if st.button("📋 GERAR RELATÓRIO E CALCULAR AR", use_container_width=True):
    
    # 1. Totais Acumulados (A base do seu cálculo que "sempre bateu")
    total_av = df_digitacao["Avaliações"].sum()
    total_res = df_digitacao["Resolvidos"].sum()
    total_vol = df_digitacao["Voltariam"].sum()
    
    # 2. Índices Globais (Como você faz no Excel)
    # Aqui a ponderação acontece naturalmente pelo volume total
    is_global = (total_res / total_av) * 100 if total_av > 0 else 0
    inn_global = (total_vol / total_av) * 100 if total_av > 0 else 0
    
    # Média Ponderada da Nota Consumidor
    # (Soma de todas as notas multiplicadas pelas suas avaliações) / Total de avaliações
    mn_global = (df_digitacao["Nota"] * df_digitacao["Avaliações"]).sum() / total_av if total_av > 0 else 0

    # 3. Fórmula AR Oficial
    ar_final = ((ir_geral * 2) + (mn_global * 10 * 3) + (is_global * 3) + (inn_global * 2)) / 100

    # --- EXIBIÇÃO ---
    st.divider()
    st.subheader(f"📊 Relatório de Performance: AR {ar_final:.2f}")
    
    # Relatório Mensal para conferência
    relatorio_mensal = df_digitacao.copy()
    relatorio_mensal["% Solução Mês"] = (relatorio_mensal["Resolvidos"] / relatorio_mensal["Avaliações"] * 100)
    relatorio_mensal["% Voltaria Mês"] = (relatorio_mensal["Voltariam"] / relatorio_mensal["Avaliações"] * 100)
    
    st.dataframe(relatorio_mensal.style.format({
        "% Solução Mês": "{:.1f}%",
        "% Voltaria Mês": "{:.1f}%",
        "Nota": "{:.2f}"
    }), use_container_width=True)

    st.markdown("### 🏆 Consolidação do Período")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nota Consumidor (MN)", f"{mn_global:.2f}")
    c2.metric("Índice Solução (IS)", f"{is_global:.1f}%")
    c3.metric("Voltaria Negócio (INN)", f"{inn_global:.1f}%")
    c4.metric("SCORE FINAL (AR)", f"{ar_final:.2f}")
