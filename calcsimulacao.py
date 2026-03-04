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
# --- BLOCO UNIFICADO: SIMULADOR DE IMPACTO ---
    st.divider()
    st.subheader("🧪 Simulador de Impacto por Lote")
    st.markdown("Veja como notas mistas afetam sua média atual nas casas decimais.")

    # Entradas de dados do lote simulado
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    with col_sim1:
        q10 = st.number_input("Qtd de Notas 10:", min_value=0, value=100, step=10, key="sim_q10")
    with col_sim2:
        q5 = st.number_input("Qtd de Notas 5:", min_value=0, value=20, step=10, key="sim_q5")
    with col_sim3:
        q0 = st.number_input("Qtd de Notas 0:", min_value=0, value=5, step=5, key="sim_q0")

    total_n = q10 + q5 + q0

    if total_n > 0:
        # Recuperando os valores que você já calculou no seu formulário principal
        # media_notas_val, indice_solucao_val e indice_novos_negocios_val
        
        # 1. Média do lote novo
        m_lote = ((q10 * 10) + (q5 * 5) + (q0 * 0)) / total_n
        
        # 2. Índices do lote novo (Considerando Nota 10 e 5 como Resolvido)
        is_lote = ((q10 * 100) + (q5 * 100) + (q0 * 0)) / total_n
        inn_lote = ((q10 * 100) + (q5 * 0) + (q0 * 0)) / total_n

        # 3. Cálculo da nova média ponderada combinando o lote com o histórico
        # Usamos total_avaliacoes que vem do seu input numérico
        n_mn = ((media_notas_val * total_avaliacoes) + (m_lote * total_n)) / (total_avaliacoes + total_n)
        n_is = ((indice_solucao_val * total_avaliacoes) + (is_lote * total_n)) / (total_avaliacoes + total_n)
        n_inn = ((indice_novos_negocios_val * total_avaliacoes) + (inn_lote * total_n)) / (total_avaliacoes + total_n)

        # 4. Resultado Final usando sua função original calcular_ar_e_ir
        n_AR, _ = calcular_ar_e_ir(total_respostas, total_reclamacoes, n_mn, n_is, n_inn)
        
        v_diff = n_AR - AR_calculado
        
        st.info(f"### Projeção com +{total_n} avaliações")
        r1, r2 = st.columns(2)
        r1.metric("Novo AR Estimado", f"{n_AR:.2f}", f"{v_diff:+.3f}")
        
        if v_diff > 0:
            st.success(f"📈 Este lote sobe sua média em **{v_diff:.3f}**.")
        else:
            st.error(f"📉 Este lote derrubaria sua média em **{abs(v_diff):.3f}**.")

st.caption("Cálculo baseado na base de 6.084 avaliações atuais.")
