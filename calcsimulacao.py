import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora RA - Pro", layout="wide")

# Estilo para destacar as linhas e colunas
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3 { color: #3cba54 !important; }
        .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Performance Mensal")
st.subheader("Controle por Mês (Cálculo Automático de Índices)")

# --- DADOS GERAIS (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Parâmetros Fixos")
    total_reclamacoes = st.number_input("Total Reclamações (Painel)", value=12774)
    total_respostas = st.number_input("Total Respostas (Painel)", value=12509)
    ir_geral = (total_respostas / total_reclamacoes) * 100 if total_reclamacoes > 0 else 0
    st.info(f"Índice de Resposta Atual: {ir_geral:.1f}%")

# --- TABELA INTERATIVA ---
st.info("Preencha a 'Qtd Solução' e 'Qtd Voltaria' para ver a porcentagem do mês aparecer na tabela abaixo.")

# Dados iniciais baseados na sua foto
dados_base = [
    {"Mês": "SETEMBRO", "Nota": 7.27, "Avaliações": 1129, "Qtd Solução": 946, "Qtd Voltaria": 889},
    {"Mês": "OUTUBRO", "Nota": 7.37, "Avaliações": 1083, "Qtd Solução": 952, "Qtd Voltaria": 899},
    {"Mês": "NOVEMBRO", "Nota": 7.42, "Avaliações": 1542, "Qtd Solução": 1342, "Qtd Voltaria": 1277},
    {"Mês": "DEZEMBRO", "Nota": 7.44, "Avaliações": 1120, "Qtd Solução": 961, "Qtd Voltaria": 922},
]

df_input = st.data_editor(
    pd.DataFrame(dados_base),
    num_rows="dynamic",
    use_container_width=True,
    key="editor_v2"
)

# --- CÁLCULOS POR LINHA (MENSAL) ---
if not df_input.empty:
    # Criamos colunas calculadas para mostrar as porcentagens mensais como no seu Excel
    df_exibicao = df_input.copy()
    
    # Cálculo das porcentagens de cada mês
    df_exibicao["% Solução Mês"] = (df_exibicao["Qtd Solução"] / df_exibicao["Avaliações"] * 100).fillna(0)
    df_exibicao["% Voltaria Mês"] = (df_exibicao["Qtd Voltaria"] / df_exibicao["Avaliações"] * 100).fillna(0)

    # Exibe a tabela com os cálculos mensais
    st.write("### ✅ Resultado Detalhado por Mês")
    # Formatando para mostrar com % e 1 casa decimal
    st.dataframe(
        df_exibicao.style.format({
            "% Solução Mês": "{:.1f}%",
            "% Voltaria Mês": "{:.1f}%",
            "Nota": "{:.2f}"
        }),
        use_container_width=True
    )

    # --- CÁLCULO DO TOTAL ACUMULADO (MÉDIA PONDERADA) ---
    t_av = df_exibicao["Avaliações"].sum()
    t_sol = df_exibicao["Qtd Solução"].sum()
    t_vol = df_exibicao["Qtd Voltaria"].sum()
    
    # Média das notas ponderada pelo volume de avaliações de cada mês
    mn_final = (df_exibicao["Nota"] * df_exibicao["Avaliações"]).sum() / t_av if t_av > 0 else 0
    is_final = (t_sol / t_av * 100) if t_av > 0 else 0
    inn_final = (t_vol / t_av * 100) if t_av > 0 else 0
    
    # Fórmula Final AR
    ar_score = ((ir_geral * 2) + (mn_final * 10 * 3) + (is_final * 3) + (inn_final * 2)) / 100

    # --- DASHBOARD DE RESULTADOS ---
    st.divider()
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Nota Consumidor (Média)", f"{mn_final:.2f}")
    res2.metric("Índice Solução Total", f"{is_final:.1f}%")
    res3.metric("Voltaria Negócio Total", f"{inn_final:.1f}%")
    res4.metric("AR FINAL ESTIMADO", f"{ar_score:.2f}")

    if ar_score >= 8:
        st.success("🎯 Com esses números, sua reputação é **RA1000**!")
    elif ar_score >= 7:
        st.info("🟢 Com esses números, sua reputação é **ÓTIMO**.")
