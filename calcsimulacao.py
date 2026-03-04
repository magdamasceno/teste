import streamlit as st

st.set_page_config(page_title="Calculadora Real RA", layout="wide")

st.title("⚖️ Calculadora de Precisão Reclame Aqui")
st.markdown("Cálculo exato baseado na fórmula: **((IR*3) + (IS*3) + (NP*2) + (NC*2)) / 10**")

# --- ENTRADA DE DADOS DO SEU PRINT ---
with st.sidebar:
    st.header("📊 Dados Reais do Painel")
    # Base Reclamações
    total_rec = st.number_input("Reclamações Totais (Ex: 12774):", value=12774)
    total_resp = st.number_input("Respondidas (Ex: 12509):", value=12509)
    
    st.divider()
    # Índices em % (Digite exatamente o que está nos círculos verdes)
    is_perc = st.number_input("Índice de Solução % (Ex: 76.3):", value=76.3)
    np_perc = st.number_input("Voltaria a Negociar % (Ex: 74.1):", value=74.1)
    nc_valor = st.number_input("Nota do Consumidor (Ex: 6.94):", value=6.94)

# --- CÁLCULO PONDERADO ---
# Transformamos as porcentagens em notas de 0 a 10 para a fórmula
ir = (total_resp / total_rec) * 10
is_nota = is_perc / 10
np_nota = np_perc / 10
nc_nota = nc_valor

# Aplicação dos Pesos
soma_pesos = (ir * 3) + (is_nota * 3) + (np_nota * 2) + (nc_nota * 2)
nota_final_calculada = soma_pesos / 10

# --- EXIBIÇÃO ---
st.subheader("📊 Resultado Final")
col1, col2 = st.columns(2)

with col1:
    st.metric("Nota Final Calculada", f"{nota_final_calculada:.2f}")
    if nota_final_calculada < 8:
        st.error("Selo Atual: BOM (Abaixo de 8.0)")
    else:
        st.success("Selo Atual: ÓTIMO")

with col2:
