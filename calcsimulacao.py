import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador de Metas RA", layout="wide")

st.title("⚖️ Simulador de Cenários e Probabilidades")
st.markdown("Insira os dados de **qualquer empresa ou período** para calcular a nota final e as projeções.")

# --- ENTRADA DE DADOS TOTALMENTE VARIÁVEL ---
with st.sidebar:
    st.header("📥 Dados de Entrada")
    
    # Campos numéricos abertos para qualquer valor
    v_tot_rec = st.number_input("Total de Reclamações:", min_value=1, value=1000)
    v_tot_resp = st.number_input("Total de Respondidas:", min_value=0, value=980)
    
    st.divider()
    
    v_tot_av = st.number_input("Total de Avaliações (com nota):", min_value=1, value=500)
    v_nc = st.number_input("Nota do Consumidor (0-10):", min_value=0.0, max_value=10.0, value=7.0, step=0.01)
    v_is = st.number_input("Índice de Solução %:", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
    v_np = st.number_input("Voltaria a Negociar %:", min_value=0.0, max_value=100.0, value=70.0, step=0.1)

# --- CÁLCULO DA NOTA ATUAL DO CENÁRIO ---
# IR (Peso 3), IS (Peso 3), NC (Peso 2), NP (2)
v_ir = (v_tot_resp / v_tot_rec) * 10
v_ar = ((v_ir * 3) + (v_is/10 * 3) + (v_np/10 * 2) + (v_nc * 2)) / 10

st.metric("Nota Final do Cenário Inserido", f"{v_ar:.2f}")

# --- TABELA DE PROBABILIDADES (PROJEÇÃO FUTURA) ---
st.divider()
st.subheader("🎯 Projeção: E se chegarem novas avaliações?")
qtd_novas = st.slider("Quantidade de novas notas para simular:", 1, 500, 50)

dados_prob = []

for n_teste in range(11):
    novo_total_av = v_tot_av + qtd_novas
    
    # Simulação: Como a nova nota afeta a média
    # Nova NC
    sim_nc = ((v_nc * v_tot_av) + (n_teste * qtd_novas)) / novo_total_av
    
    # Nova IS (Assume-se 'Resolvido' se nota >= 5)
    res_novas = qtd_novas if n_teste >= 5 else 0
    sim_is = ((v_is/100 * v_tot_av) + res_novas) / novo_total_av * 100
    
    # Nova NP (Assume-se 'Voltaria' se nota >= 7)
    vol_novas = qtd_novas if n_teste >= 7 else 0
    sim_np = ((v_np/100 * v_tot_av) + vol_novas) / novo_total_av * 100
    
    # Novo AR Final
    sim_ar = ((v_ir * 3) + (sim_is/10 * 3) + (sim_np/10 * 2) + (sim_nc * 2)) / 10
    impacto = sim_ar - v_ar
    
    dados_prob.append({
        "Nota Recebida": n_teste,
        "Nova Nota Final": round(sim_ar, 2),
        "Efeito na Média": f"{impacto:+.3f}"
    })

st.table(pd.DataFrame(dados_prob))
