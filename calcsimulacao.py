import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora RA - Estável", layout="wide")

# Estilo para evitar distrações visuais no reload
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
        [data-testid="stMetricValue"] { color: #3cba54; }
        /* Suaviza o efeito de atualização */
        .stDataFrame { transition: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Média - Magda")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    ir_geral = st.number_input("Índice de Resposta (%)", value=100.0, step=0.1)

# 1. Configuração inicial dos dados (SÓ RODA UMA VEZ)
if "dados_fixos" not in st.session_state:
    st.session_state.dados_fixos = pd.DataFrame({
        "Mês": ["SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO"],
        "Nota": [0.0] * 6,
        "Avaliações": [0] * 6,
        "Resolvidos": [0] * 6,
        "Voltariam": [0] * 6
    })

opcoes_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

# 2. O EDITOR DE DADOS (Usando a 'key' para manter o estado interno do componente)
# Isso impede que ele apague enquanto você digita.
df_editado = st.data_editor(
    st.session_state.dados_fixos,
    num_rows="fixed",
    use_container_width=True,
    key="editor_principal", # A 'key' segura os dados no lugar
    column_config={
        "Mês": st.column_config.SelectboxColumn(
            "Mês",
            options=opcoes_meses,
            required=True,
        ),
        "Nota": st.column_config.NumberColumn("Nota", format="%.2f"),
        "Avaliações": st.column_config.NumberColumn("Avaliações", step=1),
        "Resolvidos": st.column_config.NumberColumn("Resolvidos", step=1),
        "Voltariam": st.column_config.NumberColumn("Voltariam", step=1),
    }
)

# 3. BOTÃO DE CALCULAR (O cálculo só acontece aqui)
st.markdown("---")
if st.button("🚀 CALCULAR AGORA", use_container_width=True):
    # Usamos o df_editado que contém as alterações mais recentes
    res = df_editado.copy()
    
    # Cálculo das % individuais
    res["% Solução"] = (res["Resolvidos"] / res["Avaliações"] * 100).fillna(0)
    res["% Voltaria"] = (res["Voltariam"] / res["Avaliações"] * 100).fillna(0)

    # Médias Simples (Aritméticas)
    mn_simples = res["Nota"].mean()
    is_simples = res["% Solução"].mean()
    inn_simples = res["% Voltaria"].mean()

    # Score Final AR
    ar_final = ((ir_geral * 2) + (mn_simples * 10 * 3) + (is_simples * 3) + (inn_simples * 2)) / 100

    # Resultados
    st.subheader(f"🏆 Resultado Final: AR {ar_final:.2f}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Média Nota", f"{mn_simples:.2f}")
    c2.metric("Média Solução", f"{is_simples:.1f}%")
    c3.metric("Média Voltariam", f"{inn_simples:.1f}%")
