import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador de Metas GOLLOG", layout="wide")

st.title("📊 Simulador de Probabilidades e Impacto")
st.markdown("Ajuste os dados atuais e simule novos cenários para prever suas metas.")

# --- COLUNAS LATERAIS PARA DADOS ATUAIS ---
with st.sidebar:
    st.header("📌 Dados Atuais")
    total_atual = st.number_input("Total de Avaliações Atual:", min_value=1, value=100)
    nota_atual = st.number_input("Nota do Consumidor Atual:", min_value=0.0, max_value=10.0, value=8.4, step=0.1)
    
    # Porcentagens atuais (convertemos para decimal para o cálculo)
    perc_resolvidos = st.slider("Índice de Solução Atual (%):", 0, 100, 85) / 100
    perc_voltaria = st.slider("Voltaria a Negociar Atual (%):", 0, 100, 70) / 100

# --- CÁLCULO DE PROBABILIDADES (NOTA DO CONSUMIDOR) ---
st.subheader("🎯 Probabilidades para Nota do Consumidor")

col1, col2 = st.columns(2)

# Alvos de nota
alvo_sobe = round(nota_atual + 0.1, 2)
alvo_desce = round(nota_atual - 0.1, 2)

# Cálculo Matemático
# Para subir (precisamos de notas 10)
n_10_sobe = (total_atual * (alvo_sobe - nota_atual)) / (10 - alvo_sobe)
# Para cair (considerando o pior cenário: notas 0)
n_0_cai = (total_atual * (nota_atual - alvo_desce)) / alvo_desce

with col1:
    st.success(f"**Para subir para {alvo_sobe}:**")
    st.metric("Notas 10 necessárias", f"{int(n_10_sobe) + 1}")

with col2:
    st.warning(f"**Para cair para {alvo_desce}:**")
    st.metric("Notas 0 suportadas", f"{int(n_0_cai)}")

st.divider()

# --- SIMULADOR DE CENÁRIO FUTURO (IMPACTO NAS 3 MÉTRICAS) ---
st.subheader("🧪 Simular Recebimento de Novas Notas")
st.write("Se você receber um novo lote de notas agora, como ficarão seus índices?")

c1, c2, c3, c4 = st.columns(4)
novas_qtd = c1.number_input("Qtd de novas notas:", min_value=0, value=10)
nova_nota_valor = c2.selectbox("Qual nota elas terão?", list(range(11)), index=10)
nova_sol_sim = c3.checkbox("Essas notas foram 'Resolvidas'?")
nova_vol_sim = c4.checkbox("Essas notas 'Voltariam'?")

# Cálculos do Cenário Futuro
novo

