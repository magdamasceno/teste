import streamlit as st
import pandas as pd

st.set_page_config(page_title="Relatório Mensal RA", layout="wide")

# Estilo visual para o Relatório
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        .report-box { 
            background-color: #ffffff; 
            padding: 20px; 
            border-radius: 10px; 
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Gerador de Relatório Mensal - RA")

# Sidebar
with st.sidebar:
    st.header("⚙️ Parâmetros do Painel")
    ir_geral = st.number_input("Índice de Resposta Geral (%)", value=100.0, step=0.1)

# 1. Entrada de dados (Igual ao Excel)
st.subheader("1️⃣ Entrada de Dados Brutos")
st.write("Preencha os dados dos 6 meses abaixo:")

if "dados_brutos" not in st.session_state:
    st.session_state.dados_brutos = pd.DataFrame({
        "Mês": ["Mês 1", "Mês 2", "Mês 3", "Mês 4", "Mês 5", "Mês 6"],
        "Nota": [0.0] * 6,
        "Avaliações": [0] * 6,
        "Resolvidos": [0] * 6,
        "Voltariam": [0] * 6
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
        "Avaliações": st.column_config.NumberColumn("Qtd Avaliações"),
        "Resolvidos": st.column_config.NumberColumn("Qtd Resolvidos"),
        "Voltariam": st.column_config.NumberColumn("Qtd Voltariam"),
    }
)

st.markdown("---")

# 2. Botão de Processamento
if st.button("📋 GERAR RELATÓRIO MENSAL E MÉDIA FINAL", use_container_width=True):
    
    # Criando o relatório calculado
    relatorio = df_digitacao.copy()
    
    # Cálculos das porcentagens mensais (O que você precisava no relatório)
    relatorio["% Solução"] = (relatorio["Resolvidos"] / relatorio["Avaliações"] * 100).fillna(0)
    relatorio["% Voltaria"] = (relatorio["Voltariam"] / relatorio["Avaliações"] * 100).fillna(0)
    
    # Exibição do Relatório Mensal
    st.subheader("2️⃣ Relatório de Performance por Mês")
    st.write("Abaixo estão os índices calculados individualmente para cada período:")
    
    st.dataframe(
        relatorio.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%",
            "Nota": "{:.2f}"
        }),
        use_container_width=True
    )

    # 3. Cálculo da Média Simples (Aritmética do Excel)
    mn_media = relatorio["Nota"].mean()
    is_media = relatorio["% Solução"].mean()
    inn_media = relatorio["% Voltaria"].mean()

    # Fórmula AR (Média simples dos índices + IR)
    ar_final = ((ir_geral * 2) + (mn_media * 10 * 3) + (is_media * 3) + (inn_media * 2)) / 100

    # 4. Painel de Fechamento
    st.divider()
    st.subheader("3️⃣ Consolidação Final (Média Simples)")
    
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Média Nota", f"{mn_media:.2f}")
    res2.metric("Média Solução", f"{is_media:.1f}%")
    res3.metric("Média Voltaria", f"{inn_media:.1f}%")
    res4.metric("SCORE FINAL (AR)", f"{ar_final:.2f}")

    if ar_final >= 8:
        st.success("🎯 Previsão de Reputação: **RA1000**")
    elif ar_final >= 7:
        st.info("🟢 Previsão de Reputação: **ÓTIMO**")
    else:
        st.warning("🟡 Previsão de Reputação: **BOM / REGULAR**")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Média Nota", f"{mn_simples:.2f}")
    c2.metric("Média Solução", f"{is_simples:.1f}%")
    c3.metric("Média Voltariam", f"{inn_simples:.1f}%")
