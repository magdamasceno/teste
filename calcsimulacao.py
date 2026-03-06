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

st.title("📊 Calculadora de Média - Foco em Digitação")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    ir_geral = st.number_input("Índice de Resposta (%)", value=100.0, step=0.1)

# Inicializa tabela
if "dados_planilha" not in st.session_state:
    st.session_state.dados_planilha = pd.DataFrame({
        "Mês": ["SET", "OUT", "NOV", "DEZ", "JAN", "FEV"],
        "Nota": [0.0]*6,
        "Avaliações": [0]*6,
        "Resolvidos": [0]*6,
        "Voltariam": [0]*6
    })

# Editor de Dados OTIMIZADO
# O segredo para sumir a lista suspensa é o TextColumn abaixo
df_editado = st.data_editor(
    st.session_state.dados_planilha,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Mês": st.column_config.TextColumn(
            "Mês", 
            help="Digite o nome do mês",
            max_chars=20,
            validate=None  # Isso remove a lista suspensa automática
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
    res["% Solução"] = (res["Resolvidos"] / res["Avaliações"] * 100).fillna(0)
    res["% Voltaria"] = (res["Voltariam"] / res["Avaliações"] * 100).fillna(0)

    mn_simples = res["Nota"].mean()
    is_simples = res["% Solução"].mean()
    inn_simples = res["% Voltaria"].mean()

    ar_final = ((ir_geral * 2) + (mn_simples * 10 * 3) + (is_simples * 3) + (inn_simples * 2)) / 100

    st.subheader(f"🏆 Resultado Final: AR {ar_final:.2f}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Média Nota", f"{mn_simples:.2f}")
    c2.metric("Média Solução", f"{is_simples:.1f}%")
    c3.metric("Média Voltariam", f"{inn_simples:.1f}%")
