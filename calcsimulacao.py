import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Calculadora RA", layout="centered")

# Mantendo seu Estilo CSS
st.markdown("""
    <style>
        .stApp { background-color: #1B2B1F; }
        label { color: #ff69b4 !important; font-weight: bold; }
        input { font-weight: bold; }
        h1, h2, h3, p { color: white !important; font-weight: bold; }
        .stButton>button { background-color: #3cba54; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("Calculadora Reclame AQUI")

def to_float(text):
    try: return float(text.replace(',', '.'))
    except: return 0.0

# SUA FUNÇÃO ORIGINAL (Mantida para precisão total)
def calcular_ar_e_ir(respostas, reclamacoes, notas, solucao, novos_negocios):
    ir = (respostas / reclamacoes) * 100 if reclamacoes > 0 else 0
    ar_score = ((ir * 2) + (notas * 10 * 3) + (solucao * 3) + (novos_negocios * 2)) / 100
    return ar_score, ir

with st.form("formulario_principal"):
    total_reclamacoes = st.number_input("Total de reclamações", min_value=0, step=1, value=12774)
    total_respostas = st.number_input("Total de respostas", min_value=0, step=1, value=12509)
    media_notas_txt = st.text_input("Média das notas", value="6,94")
    indice_solucao_txt = st.text_input("Índice de solução (%)", value="76,3")
    indice_novos_negocios_txt = st.text_input("Índice de novos negócios (%)", value="74,1")
    total_avaliacoes = st.number_input("Total de avaliações", min_value=0, step=1, value=6084)
    submitted = st.form_submit_button("Calcular Atual e Simular")

if submitted:
    mn = to_float(media_notas_txt)
    is_val = to_float(indice_solucao_txt)
    inn = to_float(indice_novos_negocios_txt)

    AR_atual, IR_atual = calcular_ar_e_ir(total_respostas, total_reclamacoes, mn, is_val, inn)
    st.markdown(f"### Média Atual: **{AR_atual:.2f}**")

    # --- NOVA PARTE: CÁLCULO DE CASAS DECIMAIS ---
    st.divider()
    st.subheader("🎯 Projeção para Mudar a Média")
    
    col1, col2 = st.columns(2)
    
    # 1. PARA SUBIR 0.1
    alvo_subir = round(AR_atual + 0.1, 1)
    # Cálculo: Quantos '10 perfeitos' (Nota 10, IS 100, INN 100)
    # Uma nota 10 perfeita contribui com 10 pontos na média ponderada
    n_subir = (total_avaliacoes * (alvo_subir - AR_atual)) / (10 - alvo_subir)
    
    with col1:
        st.success(f"Para subir para **{alvo_subir}**")
        st.write(f"Você precisa de aproximadamente **{math.ceil(n_subir)}** avaliações '10 Perfeitas' (Nota 10 + Resolvido + Voltaria).")

    # 2. PARA CAIR 0.1
    alvo_cair = round(AR_atual - 0.1, 1)
    # Cálculo: Quantos '0 críticos' (Nota 0, IS 0, INN 0)
    n_cair = (total_avaliacoes * (AR_atual - alvo_cair)) / (alvo_cair - (IR_atual * 2 / 100))
    
    with col2:
        st.warning(f"Para cair para **{alvo_cair}**")
        st.write(f"Sua margem é de **{math.floor(abs(n_cair))}** avaliações 'Zero Críticas' (Nota 0 + Não Resolvido + Não Voltaria).")

    st.info("💡 Como sua base é grande (6.084 notas), pequenas mudanças exigem um volume alto de avaliações.")
# --- ADICIONE A PARTIR DAQUI AO FINAL DO SEU ARQUIVO ---

st.divider()
st.subheader("🧪 Simulador de Cenários Variados")
st.markdown("Em vez de apenas 'notas 10', simule um lote real de notas mistas:")

# Criando colunas para o usuário digitar a quantidade de cada nota
c1, c2, c3 = st.columns(3)
with c1:
    qtd_10 = st.number_input("Qtd de Notas 10 (Excelentes):", min_value=0, value=100, step=10)
with c2:
    qtd_5 = st.number_input("Qtd de Notas 5 (Médias):", min_value=0, value=20, step=10)
with c3:
    qtd_0 = st.number_input("Qtd de Notas 0 (Ruins):", min_value=0, value=5, step=5)

total_simulado = qtd_10 + qtd_5 + qtd_0

if total_simulado > 0:
    # Calculando os novos valores médios para o lote simulado
    # Notas: 10, 5 e 0
    nova_soma_notas = (qtd_10 * 10) + (qtd_5 * 5) + (qtd_0 * 0)
    media_notas_lote = nova_soma_notas / total_simulado
    
    # Comportamento presumido para os índices (IS e INN)
    # 10 = Sim/Sim | 5 = Sim/Não | 0 = Não/Não
    is_lote = ((qtd_10 * 100) + (qtd_5 * 100) + (qtd_0 * 0)) / total_simulado
    inn_lote = ((qtd_10 * 100) + (qtd_5 * 0) + (qtd_0 * 0)) / total_simulado

    # Mesclando com sua base histórica de 6.084 avaliações
    novo_total_av = total_avaliacoes + total_simulado
    
    # Médias Ponderadas Finais
    mn_f = ((media_notas_val * total_avaliacoes) + (media_notas_lote * total_simulado)) / novo_total_av
    is_f = ((indice_solucao_val * total_avaliacoes) + (is_lote * total_simulado)) / novo_total_av
    inn_f = ((indice_novos_negocios_val * total_avaliacoes) + (inn_lote * total_simulado)) / novo_total_av

    # Calculando o Novo AR usando a SUA função original
    novo_AR, _ = calcular_ar_e_ir(total_respostas, total_reclamacoes, mn_f, is_f, inn_f)
    
    # Diferença exata (Impacto decimal)
    variacao = novo_AR - AR_calculado
    
    # Exibição do impacto
    st.info(f"### Projeção com +{total_simulado} novas avaliações")
    res1, res2 = st.columns(2)
    res1.metric("Nova Média Estimada", f"{novo_AR:.2f}", f"{variacao:+.3f}")
    
    if variacao > 0:
        res2.success(f"Este cenário sobe sua nota em {variacao:.3f} pontos!")
    elif variacao < 0:
        res2.error(f"Este cenário derruba sua nota em {abs(variacao):.3f} pontos.")
    else:
        res2.write("Este volume de notas não é suficiente para mover a casa decimal.")

st.caption("Nota: O simulador acima projeta o impacto decimal considerando sua base atual de avaliações.")
