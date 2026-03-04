import streamlit as st

st.set_page_config(page_title="Calculadora Oficial RA", layout="wide")

st.title("⚖️ Calculadora de Probabilidade Reclame Aqui")
st.markdown("Cálculo baseado nos pesos oficiais: **IR(3), IS(3), NC(2), NP(2)**")

# --- ENTRADA DE DADOS REAIS ---
with st.sidebar:
    st.header("📊 Dados Atuais do Painel")
    reclamacoes_totais = st.number_input("Total de Reclamações Recebidas:", value=1000)
    reclamacoes_respondidas = st.number_input("Total de Respondidas:", value=990)
    
    # Índices em %
    is_perc = st.slider("Índice de Solução (IS) %:", 0, 100, 85) 
    nc_valor = st.number_input("Nota do Consumidor (NC):", 0.0, 10.0, 7.8, step=0.1)
    np_perc = st.slider("Voltaria a Fazer Negócio (NP) %:", 0, 100, 75)

# --- LÓGICA OFICIAL RECLAME AQUI ---
# IR = Índice de Resposta | IS = Índice de Solução | NC = Nota Consumidor | NP = Índice de Novos Negócios
ir = (reclamacoes_respondidas / reclamacoes_totais) * 10
is_p = (is_perc / 10)
np_p = (np_perc / 10)

# Fórmula Ponderada
nota_final_ra = ((nc_valor * 2) + (np_p * 2) + (is_p * 3) + (ir * 3)) / 10

st.subheader(f"Sua Nota Final RA Atual: {nota_final_ra:.2f}")

# --- SIMULADOR DE METAS ---
st.divider()
st.subheader("🎯 O que eu preciso para chegar em tal nota?")
alvo = st.number_input("Qual nota final você quer atingir? (Ex: 8.0)", value=8.0, step=0.1)

# Simulação simplificada: Quantas avaliações "Perfeitas" (Nota 10, Resolvida, Voltaria)
# Para simplificar a probabilidade para o usuário:
if alvo > nota_final_ra:
    # Estimativa de esforço necessário em novas avaliações nota 10/Sim/Sim
    diferenca = alvo - nota_final_ra
    esforco_estimado = (diferenca * reclamacoes_totais) / (10 - alvo)
    st.success(f"📈 Para chegar na nota **{alvo}**, você precisa de aproximadamente **{int(esforco_estimado) + 1}** avaliações PERFEITAS (Nota 10 + Solucionada + Voltaria).")
else:
    # Estimativa de queda (Notas 0/Não/Não)
    margem = nota_final_ra - alvo
    queda_suportada = (margem * reclamacoes_totais) / alvo
    st.warning(f"📉 Você aguenta aproximadamente **{int(queda_suportada)}** avaliações CRÍTICAS (Nota 0 + Não Resolvida + Não Voltaria) antes de cair para **{alvo}**.")

# --- EXPLICAÇÃO DOS PESOS ---
with st.expander("📝 Entenda como o Reclame Aqui te avalia"):
    st.write("""
    1. **Índice de Resposta (Peso 3):** Porcentagem de reclamações respondidas.
    2. **Índice de Solução (Peso 3):** Porcentagem de reclamações resolvidas (baseado no 'SIM' do consumidor).
    3. **Nota do Consumidor (Peso 2):** Média das notas de 0 a 10.
    4. **Voltaria a Fazer Negócio (Peso 2):** Porcentagem de consumidores que dizem que voltariam a negociar.
    """)
