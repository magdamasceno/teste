import streamlit as st
import pandas as pd

st.set_page_config(page_title="Relatório Mensal RA", layout="wide")

# Estilo visual que você aprovou
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Gerador de Relatório Mensal - Média Ponderada")

# Sidebar
with st.sidebar:
    st.header("⚙️ Parâmetros do Painel")
    total_reclamacoes = st.number_input("Total Reclamações", value=12774)
    total_respostas = st.number_input("Total Respostas", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta: {ir_geral:.1f}%")

st.subheader("1️⃣ Entrada de Dados Brutos")

# Inicializa os dados (com os valores do seu print)
if "dados_brutos" not in st.session_state:
    st.session_state.dados_brutos = pd.DataFrame({
        "Mês": ["OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO", "MARÇO"],
        "Nota": [7.38, 7.42, 7.44, 7.25, 7.72, 8.00],
        "Avaliações": [1086, 1542, 1129, 1144, 711, 68],
        "Resolvidos": [952, 1342, 981, 992, 619, 61],
        "Voltariam": [899, 1277, 930, 917, 590, 57]
    })

opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# EDITOR DE DADOS COM LISTA SUSPENSA
df_digitacao = st.data_editor(
    st.session_state.dados_brutos,
    num_rows="fixed",
    use_container_width=True,
    key="editor_fiel",
    column_config={
        "Mês": st.column_config.SelectboxColumn("Mês", options=opcoes_meses),
        "Nota": st.column_config.NumberColumn("Nota Consumidor", format="%.2f"),
    }
)
st.session_state.dados_brutos = df_digitacao

st.markdown("---")

if st.button("📋 GERAR RELATÓRIO MENSAL E CALCULAR AR", use_container_width=True):
    
    # 1. Relatório de Performance (Cálculo individual por mês para o relatório)
    relatorio = df_digitacao.copy()
    relatorio["% Solução"] = (relatorio["Resolvidos"] / relatorio["Avaliações"] * 100)
    relatorio["% Voltaria"] = (relatorio["Voltariam"] / relatorio["Avaliações"] * 100)
    
    st.subheader("2️⃣ Relatório de Performance por Mês")
    st.dataframe(
        relatorio.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%",
            "Nota": "{:.2f}"
        }),
        use_container_width=True
    )

    # 2. LÓGICA DE CÁLCULO FINAL (Soma tudo e divide)
    total_av_geral = df_digitacao["Avaliações"].sum()
    
    # IS e INN: Soma de todos os resolvidos / Soma de todas as avaliações
    is_total = (df_digitacao["Resolvidos"].sum() / total_av_geral) * 100 if total_av_geral > 0 else 0
    inn_total = (df_digitacao["Voltariam"].sum() / total_av_geral) * 100 if total_av_geral > 0 else 0
    
    # MN: Nota ponderada (única que exige multiplicar pela avaliação do mês antes de somar)
    mn_ponderada = (df_digitacao["Nota"] * df_digitacao["Avaliações"]).sum() / total_av_geral if total_av_geral > 0 else 0

    # 3. Fórmula Oficial do AR
    ar_final = ((ir_geral * 2) + (mn_ponderada * 10 * 3) + (is_total * 3) + (inn_total * 2)) / 100

    st.divider()
    st.subheader(f"3️⃣ Resultado Final: AR {ar_final:.2f}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nota (MN)", f"{mn_ponderada:.2f}")
    c2.metric("Solução (IS)", f"{is_total:.1f}%")
    c3.metric("Voltaria (INN)", f"{inn_total:.1f}%")
    c4.metric("SCORE FINAL (AR)", f"{ar_final:.2f}")
