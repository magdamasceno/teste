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
# --- BLOCO NOVO: SIMULADOR DE CASAS DECIMAIS VARIADAS ---
    st.divider()
    st.subheader("🧪 Simulador de Impacto por Lote")
    st.markdown("Veja como notas mistas afetam sua média atual nas casas decimais.")

    # Criando colunas para entrada de dados
    c1, c2, c3 = st.columns(3)
    with c1:
        q_10 = st.number_input("Qtd de Notas 10 (Excelentes):", min_value=0, value=100, step=10)
    with c2:
        q_5 = st.number_input("Qtd de Notas 5 (Médias):", min_value=0, value=20, step=10)
    with c3:
        q_0 = st.number_input("Qtd de Notas 0 (Ruins):", min_value=0, value=5, step=5)

    total_novas = q_10 + q_5 + q_0

    if total_novas > 0:
        # 1. Média das notas do novo lote
        media_lote = ((q_10 * 10) + (q_5 * 5) + (q_0 * 0)) / total_novas
        
        # 2. Comportamento para Índices (Baseado na sua lógica de sucesso)
        # Nota 10 = Resolvido/Voltaria | Nota 5 = Resolvido/Não | Nota 0 = Não/Não
        is_lote = ((q_10 * 100) + (q_5 * 100) + (q_0 * 0)) / total_novas
        inn_lote = ((q_10 * 100) + (q_5 * 0) + (q_0 * 0)) / total_novas

        # 3. Cálculo Ponderado com a sua base de 6.084 avaliações
        # Usando as variáveis exatas do seu código: media_notas_val, indice_solucao_val, etc.
        nova_mn = ((media_notas_val * total_avaliacoes) + (media_lote * total_novas)) / (total_avaliacoes + total_novas)
        nova_is = ((indice_solucao_val * total_avaliacoes) + (is_lote * total_novas)) / (total_avaliacoes + total_novas)
        nova_inn = ((indice_novos_negocios_val * total_avaliacoes) + (inn_lote * total_novas)) / (total_avaliacoes + total_novas)

        # 4. Calculando o Novo AR com a sua função oficial
        novo_AR, _ = calcular_ar_e_ir(total_respostas, total_reclamacoes, nova_mn, nova_is, nova_inn)
        
        # 5. Exibição da Variação Decimal
        variacao = novo_AR - AR_calculado
        
        st.info(f"### Projeção com +{total_novas} avaliações")
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Novo AR Estimado", f"{novo_AR:.2f}", f"{variacao:+.3f}")
        
        if variacao > 0:
            st.success(f"📈 Este lote de notas sobe sua média em **{variacao:.3f}**. Faltam {(0.1 - variacao):.3f} para subir uma casa decimal inteira (0.1).")
        else:
            st.error(f"📉 Este lote de notas derrubaria sua média em **{abs(variacao):.3f}**.")

st.caption("Nota: O cálculo acima projeta o impacto real nas casas decimais considerando o 'peso' das avaliações anteriores.")

