import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Calculadora RA - Pro", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
        .stApp { background-color: #111b15; }
        h1, h2, h3 { color: #3cba54 !important; }
        .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Calculadora de Performance RA (Mensal)")

# --- CONFIGURAÇÃO INICIAL (PAINEL LATERAL) ---
with st.sidebar:
    st.header("⚙️ Dados Fixos do Período")
    # Valores padrão baseados nos seus prints anteriores
    total_reclamacoes = st.number_input("Total Reclamações (Geral)", value=12774)
    total_respostas = st.number_input("Total Respostas (Geral)", value=12509)

# --- TABELA ESTILO EXCEL (6 MESES EM BRANCO) ---
st.subheader("📝 Preencha os dados brutos dos meses")
st.info("Insira as quantidades de 'Resolvidos' e 'Voltariam'. O sistema calculará as % sozinho.")

# Criando a estrutura com 6 meses vazios
meses_vazios = [
    {"Mês": "Setembro", "Nota Consumidor": 0.0, "Resolvidos": 0, "Voltariam": 0, "Avaliações": 0},
    {"Mês": "Outubro", "Nota Consumidor": 0.0, "Resolvidos": 0, "Voltariam": 0, "Avaliações": 0},
    {"Mês": "Novembro", "Nota Consumidor": 0.0, "Resolvidos": 0, "Voltariam": 0, "Avaliações": 0},
    {"Mês": "Dezembro", "Nota Consumidor": 0.0, "Resolvidos": 0, "Voltariam": 0, "Avaliações": 0},
    {"Mês": "Janeiro", "Nota Consumidor": 0.0, "Resolvidos": 0, "Voltariam": 0, "Avaliações": 0},
    {"Mês": "Fevereiro", "Nota Consumidor": 0.0, "Resolvidos": 0, "Voltariam": 0, "Avaliações": 0},
]

df_editor = st.data_editor(
    pd.DataFrame(meses_vazios),
    num_rows="dynamic", # Permite que você adicione mais que 6 meses se quiser
    column_config={
        "Mês": st.column_config.TextColumn("Mês", required=True),
        "Nota Consumidor": st.column_config.NumberColumn("Média Nota (0-10)", min_value=0.0, max_value=10.0, format="%.2f"),
        "Resolvidos": st.column_config.NumberColumn("Qtd de Resolvidos", min_value=0),
        "Voltariam": st.column_config.NumberColumn("Qtd Voltariam Negócio", min_value=0),
        "Avaliações": st.column_config.NumberColumn("Total de Avaliações", min_value=0),
    },
    use_container_width=True,
    key="editor_vazio"
)

# --- LÓGICA DE CÁLCULO DINÂMICO ---
# Filtra apenas linhas onde o usuário preencheu avaliações para evitar divisão por zero
df_filtrado = df_editor[df_editor["Avaliações"] > 0]

if not df_filtrado.empty:
    # Totais Acumulados do Período
    total_av = df_filtrado["Avaliações"].sum()
    total_res = df_filtrado["Resolvidos"].sum()
    total_vol = df_filtrado["Voltariam"].sum()
    
    # Médias Ponderadas
    mn_final = (df_filtrado["Nota Consumidor"] * df_filtrado["Avaliações"]).sum() / total_av
    
    # Índices em % (Cálculo Automático solicitado)
    is_final = (total_res / total_av) * 100
    inn_final = (total_vol / total_av) * 100
    ir_final = (total_respostas / total_reclamacoes) * 100

    # Fórmula Oficial do Reclame Aqui
    ar_score = ((ir_final * 2) + (mn_final * 10 * 3) + (is_final * 3) + (inn_final * 2)) / 100

    # --- EXIBIÇÃO DOS RESULTADOS ---
    st.divider()
    st.subheader("🎯 Resultado Acumulado dos Meses")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Média Nota (MN)", f"{mn_final:.2f}")
    c2.metric("Índice Solução (IS)", f"{is_final:.1f}%")
    c3.metric("Voltaria Negócio (INN)", f"{inn_final:.1f}%")
    c4.metric("NOTA FINAL (AR)", f"{ar_score:.2f}")

    # Indicação de Reputação
    if ar_score >= 8: st.success("🏆 Status Estimado: **RA1000**")
    elif ar_score >= 7: st.info("🟢 Status Estimado: **ÓTIMO**")
    elif ar_score >= 6: st.warning("🟡 Status Estimado: **BOM**")
    else: st.error("🔴 Status Estimado: **REGULAR / RUIM**")
else:
    st.warning("⚠️ Preencha os dados de pelo menos um mês na tabela acima para ver o cálculo.")
