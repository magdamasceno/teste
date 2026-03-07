import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora RA Oficial", layout="wide")

# Estilo Visual
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora RA - Modelo de Soma Bruta")

# Sidebar para o IR Geral do Painel
with st.sidebar:
    st.header("⚙️ Configuração")
    total_reclamacoes = st.number_input("Total Reclamações (Painel)", value=12774)
    total_respostas = st.number_input("Total Respondidas (Painel)", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta: {ir_geral:.1f}%")

st.subheader("1️⃣ Preencha os Dados Mensais")

# Lista suspensa de meses
opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# Tabela inicia EM BRANCO (sem resultados carregados)
if "tabela_limpa" not in st.session_state:
    st.session_state.tabela_limpa = pd.DataFrame({
        "Mês": ["Mês 1", "Mês 2", "Mês 3", "Mês 4", "Mês 5", "Mês 6"],
        "Nota": [0.0]*6,
        "Avaliações": [0]*6,
        "Resolvidos": [0]*6,
        "Voltariam": [0]*6
    })

# Editor com Lista Suspensa
df_input = st.data_editor(
    st.session_state.tabela_limpa,
    num_rows="fixed",
    use_container_width=True,
    key="editor_v4",
    column_config={
        "Mês": st.column_config.SelectboxColumn("Mês", options=opcoes_meses),
        "Nota": st.column_config.NumberColumn("Nota Consumidor", format="%.2f"),
    }
)

st.markdown("---")

# SÓ CALCULA AO CLICAR NO BOTÃO
if st.button("🚀 GERAR RELATÓRIO E CALCULAR AR", use_container_width=True):
    
    # Filtra apenas linhas onde houve avaliações para não dar erro de divisão por zero
    df_validos = df_input[df_input["Avaliações"] > 0].copy()
    
    if not df_validos.empty:
        # TOTAIS ACUMULADOS (A base que você usa no Excel)
        soma_av = df_validos["Avaliações"].sum()
        soma_res = df_validos["Resolvidos"].sum()
        soma_vol = df_validos["Voltariam"].sum()

        # ÍNDICES GERAIS (Soma dos Resolvidos / Soma das Avaliações)
        is_global = (soma_res / soma_av) * 100
        inn_global = (soma_vol / soma_av) * 100
        
        # NOTA PONDERADA (Única que multiplica cada linha antes de somar)
        mn_ponderada = (df_validos["Nota"] * df_validos["Avaliações"]).sum() / soma_av

        # FÓRMULA AR OFICIAL
        ar_final = ((ir_geral * 2) + (mn_ponderada * 10 * 3) + (is_global * 3) + (inn_global * 2)) / 100

        # RELATÓRIO MENSAL (Calculado apenas para visualização)
        st.subheader("2️⃣ Relatório de Performance Mensal")
        df_validos["% Solução"] = (df_validos["Resolvidos"] / df_validos["Avaliações"] * 100)
        df_validos["% Voltaria"] = (df_validos["Voltariam"] / df_validos["Avaliações"] * 100)
        
        st.dataframe(df_validos.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%",
            "Nota": "{:.2f}"
        }), use_container_width=True)

        # MÉTRICAS FINAIS
        st.divider()
        st.subheader(f"3️⃣ Resultado Final: AR {ar_final:.2f}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Nota (MN)", f"{mn_ponderada:.2f}")
        col2.metric("Solução (IS)", f"{is_global:.1f}%")
        col3.metric("Voltaria (INN)", f"{inn_global:.1f}%")
        col4.metric("SCORE FINAL", f"{ar_final:.2f}")
    else:
        st.warning("Por favor, preencha os dados de 'Avaliações' para calcular.")
