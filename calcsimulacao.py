import streamlit as st
import pandas as pd

st.set_page_config(page_title="Média Últimos 6 Meses", layout="wide")

# Estilo visual
st.markdown("""
    <style>
        [data-testid="stMetricValue"] { font-size: 25px; color: #3cba54; }
        .stApp { background-color: #111b15; }
        h1, h2, h3, p { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Média Simples - 6 Meses")

# Lista de todos os meses para a lista suspensa
MESES_LISTA = [
    "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]

with st.sidebar:
    st.header("⚙️ Dados Fixos")
    ir_geral = st.number_input("Índice de Resposta Geral (%)", value=98.0, step=0.1)

st.write("Selecione os meses na lista suspensa e insira os dados brutos.")

# Inicialização da tabela com meses vazios ou pré-definidos
if "tabela" not in st.session_state:
    st.session_state.tabela = pd.DataFrame({
        "Mês": ["SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO", "JANEIRO", "FEVEREIRO"],
        "Nota Consumidor": [7.27, 7.37, 7.42, 7.44, 7.25, 7.72],
        "Total Avaliações": [1129, 1083, 1542, 1120, 1144, 711],
        "Total Solução": [946, 952, 1342, 961, 992, 619],
        "Total Voltaria": [889, 899, 1277, 922, 917, 590]
    })

# Editor de Dados com COLUNA DE SELEÇÃO (Selectbox)
df = st.data_editor(
    st.session_state.tabela,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Mês": st.column_config.SelectboxColumn(
            "Selecione o Mês",
            help="Escolha o mês correspondente",
            width="medium",
            options=MESES_LISTA,
            required=True,
        ),
        "Nota Consumidor": st.column_config.NumberColumn("Nota", format="%.2f"),
        "Total Avaliações": st.column_config.NumberColumn("Avaliações"),
        "Total Solução": st.column_config.NumberColumn("Qtd Resolvidos"),
        "Total Voltaria": st.column_config.NumberColumn("Qtd Voltariam")
    }
)
st.session_state.tabela = df

# BOTÃO DE COMANDO
st.markdown("---")
btn_calcular = st.button("🚀 CALCULAR MÉDIA SIMPLES", use_container_width=True)

if btn_calcular:
    df_result = df.copy()
    # Cálculo das porcentagens por linha
    df_result["% Solução"] = (df_result["Total Solução"] / df_result["Total Avaliações"] * 100).fillna(0)
    df_result["% Voltaria"] = (df_result["Total Voltaria"] / df_result["Total Avaliações"] * 100).fillna(0)

    st.subheader("📈 Detalhamento Mensal")
    st.dataframe(
        df_result.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%",
            "Nota Consumidor": "{:.2f}"
        }), use_container_width=True
    )

    # MÉDIA SIMPLES (IGUAL AO EXCEL)
    mn_simples = df_result["Nota Consumidor"].mean()
    is_simples = df_result["% Solução"].mean()
    inn_simples = df_result["% Voltaria"].mean()

    ar_final = ((ir_geral * 2) + (mn_simples * 10 * 3) + (is_simples * 3) + (inn_simples * 2)) / 100

    st.divider()
    st.subheader(f"🏆 Resultado Final: AR {ar_final:.2f}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Média Nota Consumidor", f"{mn_simples:.2f}")
    m2.metric("Média % Solução", f"{is_simples:.1f}%")
    m3.metric("Média % Voltaria", f"{inn_simples:.1f}%")
    m4.metric("AR Final", f"{ar_final:.2f}")
