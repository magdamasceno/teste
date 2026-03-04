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

# --- FORMULÁRIO DE DADOS FIXOS ---
with st.form("formulario_principal"):
    total_reclamacoes = st.number_input("Total de reclamações", min_value=0, step=1, value=12774)
    total_respostas = st.number_input("Total de respostas", min_value=0, step=1, value=12509)
    media_notas_txt = st.text_input("Média das notas", value="6,94")
    indice_solucao_txt = st.text_input("Índice de solução (%)", value="76,3")
    indice_novos_negocios_txt = st.text_input("Índice de novos negócios (%)", value="74,1")
    total_avaliacoes = st.number_input("Total de avaliações", min_value=0, step=1, value=6084)
    btn_calcular = st.form_submit_button("Fixar Dados e Liberar Simulador")

# Inicializa o estado de memória se não existir
if 'clicado' not in st.session_state:
    st.session_state.clicado = False

if btn_calcular:
    st.session_state.clicado = True

# --- EXIBIÇÃO DOS RESULTADOS (SÓ APARECE APÓS CLICAR) ---
if st.session_state.clicado:
    mn_atual = to_float(media_notas_txt)
    is_atual = to_float(indice_solucao_txt)
    inn_atual = to_float(indice_novos_negocios_txt)

    AR_atual, IR_atual = calcular_ar_e_ir(total_respostas, total_reclamacoes, mn_atual, is_atual, inn_atual)
    
    st.markdown(f"### Média Atual do Painel: **{AR_atual:.2f}**")

    # Simulador de Lote (FORA DO FORMULÁRIO para ser interativo)
    st.divider()
    st.subheader("🧪 Simulador Interativo de Notas")
    st.write("Altere os números abaixo para ver a média mudar em tempo real:")

    col_s1, col_s2, col_s3 = st.columns(3)
    q10 = col_s1.number_input("Qtd de Notas 10:", min_value=0, value=257, step=10)
    q5 = col_s2.number_input("Qtd de Notas 5:", min_value=0, value=0, step=10)
    q0 = col_s3.number_input("Qtd de Notas 0:", min_value=0, value=0, step=10)

    total_n = q10 + q5 + q0

    if total_n > 0:
        m_lote = ((q10 * 10) + (q5 * 5) + (q0 * 0)) / total_n
        is_lote = ((q10 * 100) + (q5 * 100) + (q0 * 0)) / total_n
        inn_lote = ((q10 * 100) + (q5 * 0) + (q0 * 0)) / total_n

        nova_mn = ((mn_atual * total_avaliacoes) + (m_lote * total_n)) / (total_avaliacoes + total_n)
        nova_is = ((is_atual * total_avaliacoes) + (is_lote * total_n)) / (total_avaliacoes + total_n)
        nova_inn = ((inn_atual * total_avaliacoes) + (inn_lote * total_n)) / (total_avaliacoes + total_n)

        n_AR, _ = calcular_ar_e_ir(total_respostas, total_reclamacoes, nova_mn, nova_is, nova_inn)
        diff = n_AR - AR_atual
        
        st.info(f"### Resultado Projetado: **{n_AR:.2f}**")
        st.metric("Variação Decimal", f"{n_AR:.3f}", f"{diff:+.3f}")
        
        if n_AR >= round(AR_atual + 0.1, 1):
            st.success("✅ Com este lote você sobe uma casa decimal!")
        else:
            st.warning(f"Faltam {(round(AR_atual + 0.1, 1) - n_AR):.3f} para subir para {round(AR_atual + 0.1, 1)}")
