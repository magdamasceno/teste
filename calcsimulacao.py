import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora RA - 6 Meses", layout="wide")

# CSS para melhorar o foco visual na tabela
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3 { color: #3cba54 !important; }
        /* Deixa a tabela com cara de planilha focada */
        [data-testid="stDataFrame"] { border: 2px solid #3cba54; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora Mensal Simples")
st.info("💡 Dica de digitação: Digite o número e aperte **ENTER** para pular para a linha de baixo automaticamente.")

# Sidebar com IR fixo
with st.sidebar:
    st.header("⚙️ Configuração")
    ir_geral = st.number_input("Índice de Resposta (%)", value=100.0, step=0.1)

# Inicializa tabela vazia se não existir
if "dados_planilha" not in st.session_state:
    st.session_state.dados_planilha = pd.DataFrame({
        "Mês": ["Mês 1", "Mês 2", "Mês 3", "Mês 4", "Mês 5", "Mês 6"],
        "Nota": [0.0]*6,
        "Avaliações": [0]*6,
        "Resolvidos": [0]*6,
        "Voltariam": [0]*6
    })

# Editor de Dados (Configurado para facilitar a navegação)
df_editado = st.data_editor(
    st.session_state.dados_planilha,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Nota": st.column_config.NumberColumn(format="%.2f"),
        "Avaliações": st.column_config.NumberColumn(step=1),
        "Resolvidos": st.column_config.NumberColumn(step=1),
        "Voltariam": st.column_config.NumberColumn(step=1),
    }
)

# Salva o estado para não perder nada ao interagir
st.session_state.dados_planilha = df_editado

st.markdown("---")
if st.button("🚀 CALCULAR MÉDIA DOS 6 MESES", use_container_width=True):
    
    # 1. Cálculos Mensais Individuais
    res = df_editado.copy()
    # Evita divisão por zero se a célula estiver vazia
    res["% Solução"] = (res["Resolvidos"] / res["Avaliações"] * 100).fillna(0)
    res["% Voltaria"] = (res["Voltariam"] / res["Avaliações"] * 100).fillna(0)

    # 2. Médias Simples (Aritméticas)
    mn_simples = res["Nota"].mean()
    is_simples = res["% Solução"].mean()
    inn_simples = res["% Voltaria"].mean()

    # 3. Fórmula AR (Média das porcentagens + IR)
    ar_final = ((ir_geral * 2) + (mn_simples * 10 * 3) + (is_simples * 3) + (inn_simples * 2)) / 100

    # Exibição dos resultados
    st.subheader(f"📊 Resultado Final: AR {ar_final:.2f}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Média das Notas", f"{mn_simples:.2f}")
    c2.metric("Média Solução", f"{is_simples:.1f}%")
    c3.metric("Média Voltariam", f"{inn_simples:.1f}%")
    
    # Tabela de conferência
    with st.expander("Ver detalhes calculados por mês"):
        st.dataframe(res.style.format({
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%"
        }), use_container_width=True)
