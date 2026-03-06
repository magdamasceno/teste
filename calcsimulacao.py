import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora RA - 6 Meses", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Média - Com Lista Suspensa")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    ir_geral = st.number_input("Índice de Resposta (%)", value=100.0, step=0.1)

# Lista de meses para a lista suspensa
opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# Inicializa tabela
if "dados_planilha" not in st.session_state:
    st.session_state.dados_planilha = pd.DataFrame({
        "Mês": ["SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO"],
        "Nota": [0.0]*6,
        "Avaliações": [0]*6,
        "Resolvidos": [0]*6,
        "Voltariam": [0]*6
    })

# Editor de Dados com SELECTBOX (Lista Suspensa)
df_editado = st.data_editor(
    st.session_state.dados_planilha,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Mês": st.column_config.SelectboxColumn(
            "Mês",
            help="Selecione o mês",
            options=opcoes_meses, # Aqui define a lista suspensa
            required=True,
        ),
        "Nota": st.column_config.NumberColumn("Nota", format="%.2f", min_value=0.0, max_value=10.0),
        "Avaliações": st.column_config.NumberColumn("Avaliações", step=1),
        "Resolvidos": st.column_config.NumberColumn("Resolvidos", step=1),
        "Voltariam": st.column_config.NumberColumn("Voltariam", step=1),
    }
)

st.session_state.dados_planilha = df_editado

st.markdown("---")
if st.button("🚀 CALCULAR MÉDIA SIMPLES", use_container_width=True):
    # Lógica de Média Simples (Igual ao Excel)
    res = df_editado.copy()
    
    # Cálculo das porcentagens individuais de cada mês
    res["% Solução"] = (res["Resolvidos"] / res["Avaliações"] * 100).fillna(0)
    res["% Voltaria"] = (res["Voltariam"] / res["Avaliações"] * 100).fillna(0)

    # Tirando a média simples das porcentagens e da nota
    mn_simples = res["Nota"].mean()
    is_simples = res["% Solução"].mean()
    inn_simples = res["% Voltaria"].mean()

    # AR Final (Fórmula Reclame AQUI)
    ar_final = ((ir_geral * 2) + (mn_simples * 10 * 3) + (is_simples * 3) + (inn_simples * 2)) / 100

    st.subheader(f"🏆 Resultado Final: AR {ar_final:.2f}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Média Nota", f"{mn_simples:.2f}")
    c2.metric("Média Solução", f"{is_simples:.1f}%")
    c3.metric("Média Voltariam", f"{inn_simples:.1f}%")
