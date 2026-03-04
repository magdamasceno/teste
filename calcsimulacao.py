import streamlit as st

st.set_page_config(page_title="Calculadora RA Smiles", layout="wide")

st.title("⚖️ Calculadora de Precisão Reclame Aqui")
st.info("💡 Para bater com os 7.8 do seu painel, use apenas os dados do período atual (6 ou 12 meses).")

# --- ENTRADA DE DADOS EXATOS ---
with st.sidebar:
    st.header("📊 Dados do Painel")
    
    # Base Reclamações (Usada para o Índice de Resposta)
    tot_rec = st.number_input("Total de Reclamações do Período:", value=12774)
    tot_resp = st.number_input("Reclamações Respondidas:", value=12509)
    
    st.divider()
    
    # Base Avaliações (Ouro: Onde a nota do consumidor nasce)
    tot_av = st.number_input("Total de Avaliações (Com nota):", value=6084)
    
    # Índices exatos (Digite exatamente o que aparece no círculo verde)
    nc_atual = st.number_input("Nota do Consumidor (Ex: 6.94):", value=6.94, step=0.01)
    is_atual = st.number_input("Índice de Solução % (Ex: 76.3):", value=76.3, step=0.1)
    np_atual = st.number_input("Voltaria a Negociar % (Ex: 74.1):", value=74.1, step=0.1)

# --- FÓRMULA OFICIAL DO RECLAME AQUI ---
# 1. Índice de Resposta (Peso 3)
ir = (tot_resp / tot_rec) * 10
# 2. Índice de Solução (Peso 3)
is_p = is_atual / 10
# 3. Voltaria a Fazer Negócio (Peso 2)
np_p = np_atual / 10
# 4. Nota do Consumidor (Peso 2)
nc_p = nc_atual

# Cálculo Final Ponderado
nota_ra = ((ir * 3) + (is_p * 3) + (np_p * 2) + (nc_p * 2)) / 10

# --- EXIBIÇÃO ---
st.subheader("📊 Resultado do Período")
c1, c2 = st.columns(2)

c1.metric("Nota Final Calculada", f"{nota_ra:.2f}")
c2.write(f"""
**Pesos Aplicados:**
* Índice de Resposta: {ir:.2f} (Peso 3)
* Índice de Solução: {is_p:.2f} (Peso 3)
* Voltaria a Negociar: {np_p:.2f} (Peso 2)
* Nota do Consumidor: {nc_p:.2f} (Peso 2)
""")

# --- SIMULADOR DE PROBABILIDADE ---
st.divider()
st.subheader("🎯 O que falta para subir?")

meta = st.number_input("Qual nota final você deseja atingir? (Ex: 8.0)", value=8.0, step=0.1)

if meta > nota_ra:
    # Cálculo de quantas avaliações "Perfeitas" (Nota 10, Sim, Sim) são necessárias
    # A fórmula considera o 'peso' que cada avaliação nova tem sobre a base atual de 6.084
    diff = meta - nota_ra
    # Impacto de uma nota 10/Sim/Sim na média final
    impacto_nota_10 = ((10*2 + 10*3 + 10*2 + ir*3)/10) - meta
    necessarias = (diff * tot_av) / impacto_nota_10
    
    st.success(f"📈 Para chegar em **{meta}**, você precisa de aproximadamente **{int(necessarias) + 1}** avaliações 'Perfeitas' (Nota 10 + Solucionada + Voltaria).")
else:
    st.warning("Meta já atingida.")
