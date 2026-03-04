import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora RA Smiles", layout="wide")

st.title("⚖️ Calculadora de Probabilidades Reclame Aqui")
st.markdown("Simulação baseada na fórmula oficial: **((IR*3) + (IS*3) + (NP*2) + (NC*2)) / 10**")

# --- ENTRADA DE DADOS EXATOS DO SEU PAINEL ---
with st.sidebar:
    st.header("📊 Dados Atuais")
    # Base Reclamações (IR)
    tot_rec = st.number_input("Total de Reclamações:", value=12774)
    tot_resp = st.number_input("Reclamações Respondidas:", value=12509)
    st.divider()
    # Base Avaliações (IS, NP, NC)
    tot_av = st.number_input("Total de Avaliações (Ouro):", value=6084)
    nc_atual = st.number_input("Nota do Consumidor Atual:", value=6.94)
    is_atual = st.number_input("Índice de Solução Atual (%):", value=76.3)
    np_atual = st.number_input("Voltaria a Negociar Atual (%):", value=74.1)

# --- CÁLCULO DA NOTA REAL AGORA ---
ir = (tot_resp / tot_rec) * 10
nota_ra_atual = ((ir * 3) + (is_atual/10 * 3) + (np_atual/10 * 2) + (nc_atual * 2)) / 10

st.metric("Sua Nota Final Atual", f"{nota_ra_atual:.2f}")

# --- TABELA DE TODAS AS POSSIBILIDADES ---
st.subheader("🎯 Simulador de Impacto por Nota")
st.write("Se você receber **100 novas avaliações** com a mesma nota, como fica seu painel?")

simulacoes = []

for nota_teste in range(11): # Testa de 0 a 10
    novo_tot_av = tot_av + 100
    
    # Nova Nota Consumidor
    nova_nc = ((nc_atual * tot_av) + (nota_teste * 100)) / novo_tot_av
    
    # Novo Índice de Solução (Considerando que nota >= 5 é Resolvido)
    resolvido = 100 if nota_teste >= 5 else 0
    nova_is = ((is_atual/100 * tot_av) + resolvido) / novo_tot_av * 100
    
    # Novo Voltaria a Negociar (Considerando que nota >= 7 é Voltaria)
    voltaria = 100 if nota_teste >= 7 else 0
    nova_np = ((np_atual/100 * tot_av) + voltaria) / novo_tot_av * 100
    
    # Cálculo Final com Pesos
    nova_final = ((ir * 3) + (nova_is/10 * 3) + (nova_np/10 * 2) + (nova_nc * 2)) / 10
    diff = nova_final - nota_ra_atual
    
    simulacoes.append({
        "Nota Recebida": nota_teste,
        "Nova Nota Final": round(nova_final, 2),
        "Impacto": f"{diff:+.3f}"
    })

df_sim = pd.DataFrame(simulacoes)
st.table(df_sim)

st.warning("⚠️ Nota: O simulador acima assume que notas baixas (0-4) vêm acompanhadas de 'Não Resolvido' e 'Não Voltaria', conforme o comportamento padrão do consumidor.")
