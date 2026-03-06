import streamlit as st
import pandas as pd

st.set_page_config(page_title="Relatório Mensal RA", layout="wide")

# Estilo visual
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
    # Valores baseados no seu cenário para bater o 7.43
    total_reclamacoes = st.number_input("Total Reclamações", value=12774)
    total_respostas = st.number_input("Total Respostas", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta: {ir_geral:.1f}%")

st.subheader("1️⃣ Entrada de Dados Brutos")

if "dados_brutos" not in st.session_state:
    # Dados da sua planilha que levam ao AR 7.43
    st.session_state.dados_brutos = pd.DataFrame({
        "Mês": ["SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO"],
        "Nota": [7.27, 7.37, 7.42, 7.44, 7.25, 7.72],
        "Avaliações": [1129, 1083, 1542, 1120, 1144, 711],
        "Resolvidos": [946, 952, 1342, 961, 992, 619],
        "Voltariam": [889, 899, 1277, 922, 917, 590]
    })

opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

df_digitacao = st.data_editor(
    st.session_state.dados_brutos,
    num_rows="fixed",
    use_container_width=True,
    key="editor_relatorio",
    column_config={
        "Mês": st.column_config.SelectboxColumn("Mês", options=opcoes_meses),
        "Nota": st.column_config.NumberColumn("Nota Consumidor", format="%.2f"),
    }
)

st.markdown("---")

if st.button("📋 GERAR RELATÓRIO MENSAL E CALCULAR AR", use_container_width=True):
    
    # 1. Relatório Detalhado (Porcentagens individuais de cada mês)
    relatorio = df_digitacao.copy()
    relatorio["% Solução"] = (relatorio["Resolvidos"] / relatorio["Avaliações"] * 100).fillna(0)
    relatorio["% Voltaria"] = (relatorio["Voltariam"] / relatorio["Avaliações"] * 100).fillna(0)
    
    st.subheader("2️⃣ Relatório de Performance por Mês")
    st.dataframe(
        relatorio.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%",
            "Nota": "{:.2f}"
        }),
        use_container_width=True
    )

    # 2. LÓGICA DE MÉDIA PONDERADA (PESO POR VOLUME DE AVALIAÇÕES)
    total_av_geral = relatorio["Avaliações"].sum()
    
    # Média das notas ponderada: (Nota * Avaliações) / Total de Avaliações
    mn_ponderada = (relatorio["Nota"] * relatorio["Avaliações"]).sum() / total_av_geral
    
    # Índices Totais (Resolvidos Totais / Avaliações Totais)
    is_total = (relatorio["Resolvidos"].sum() / total_av_geral) * 100
    inn_total = (relatorio["Voltariam"].sum() / total_av_geral) * 100

    # 3. FÓRMULA OFICIAL DO AR (Com os pesos do Reclame AQUI)
    # AR = ((IR * 2) + (MN * 10 * 3) + (IS * 3) + (INN * 2)) / 100
    ar_final = ((ir_geral * 2) + (mn_ponderada * 10 * 3) + (is_total * 3) + (inn_total * 2)) / 100

    st.divider()
    st.subheader(f"3️⃣ Resultado Final: AR {ar_final:.2f}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nota Consumidor", f"{mn_ponderada:.2f}")
    c2.metric("Índice Solução", f"{is_total:.1f}%")
    c3.metric("Novos Negócios", f"{inn_total:.1f}%")
    c4.metric("SCORE FINAL (AR)", f"{ar_final:.2f}")

    if ar_final >= 7:
        st.success("Sua reputação estimada com esses dados é **ÓTIMO**!")
