import streamlit as st
import math

st.set_page_config(page_title="Calculadora RA", layout="centered")

# Estilo CSS
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
    # 1. PROCESSAMENTO INICIAL
    mn_atual = to_float(media_notas_txt)
    is_atual = to_float(indice_solucao_txt)
    inn_atual = to_float(indice_novos_negocios_txt)

    AR_atual, IR_atual = calcular_ar_e_ir(total_respostas, total_reclamacoes, mn_atual, is_atual, inn_atual)
    st.markdown(f"### Média Atual: **{AR_atual:.2f}**")

    # 2. PROJEÇÃO PARA MUDAR 0.1 (O QUE VOCÊ JÁ TINHA)
    st.divider()
    st.subheader("🎯 Projeção para Mudar a Média")
    col1, col2 = st.columns(2)
    
    alvo_subir = round(AR_atual + 0.1, 1)
    n_subir = (total_avaliacoes * (alvo_subir - AR_atual)) / (10 - alvo_subir)
    
    with col1:
        st.success(f"Para subir para **{alvo_subir}**")
        st.write(f"Você precisa de ~**{math.ceil(n_subir)}** avaliações '10 Perfeitas'.")

    alvo_cair = round(AR_atual - 0.1, 1)
    divisor_cair = (alvo_cair - (IR_atual * 2 / 100))
    n_cair = (total_avaliacoes * (AR_atual - alvo_cair)) / divisor_cair if divisor_cair != 0 else 0
    
    with col2:
        st.warning(f"Para cair para **{alvo_cair}**")
        st.write(f"Sua margem é de ~**{math.floor(abs(n_cair))}** avaliações 'Zero Críticas'.")

    # 3. SIMULADOR DE IMPACTO POR LOTE (O NOVO BLOCO)
    st.divider()
    st.subheader("🧪 Simulador de Impacto por Lote")
    st.markdown("Como um lote misto afeta as casas decimais:")

    col_s1, col_s2, col_s3 = st.columns(3)
    q10 = col_s1.number_input("Qtd de Notas 10:", min_value=0, value=100, key="sim_10")
    q5 = col_s2.number_input("Qtd de Notas 5:", min_value=0, value=20, key="sim_5")
    q0 = col_s3.number_input("Qtd de Notas 0:", min_value=0, value=5, key="sim_0")

    total_n = q10 + q5 + q0

    if total_n > 0:
        # Médias do lote novo
        m_lote = ((q10 * 10) + (q5 * 5) + (q0 * 0)) / total_n
        is_lote = ((q10 * 100) + (q5 * 100) + (q0 * 0)) / total_n
        inn_lote = ((q10 * 100) + (q5 * 0) + (q0 * 0)) / total_n

        # Fusão ponderada (Usando mn_atual, is_atual e inn_atual definidos no passo 1)
        nova_mn = ((mn_atual * total_avaliacoes) + (m_lote * total_n)) / (total_avaliacoes + total_n)
        nova_is = ((is_atual * total_avaliacoes) + (is_lote * total_n)) / (total_avaliacoes + total_n)
        nova_inn = ((inn_atual * total_avaliacoes) + (inn_lote * total_n)) / (total_avaliacoes + total_n)

        # Novo AR
        n_AR, _ = calcular_ar_e_ir(total_respostas, total_reclamacoes, nova_mn, nova_is, nova_inn)
        v_diff = n_AR - AR_atual
        
        st.info(f"### Resultado com +{total_n} notas mistas")
        r1, r2 = st.columns(2)
        r1.metric("Novo AR Projetado", f"{n_AR:.2f}", f"{v_diff:+.3f}")
        
        if v_diff > 0:
            st.success(f"Sobe **{v_diff:.3f}** pontos.")
        else:
            st.error(f"Cai **{abs(v_diff):.3f}** pontos.")
