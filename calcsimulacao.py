Import streamlit as st

import pandas as pd



st.set_page_config(page_title="Média Últimos 6 Meses", layout="wide")



st.title("📊 Calculadora de Média - Últimos 6 Meses")



st.write("Preencha os dados. Você pode alterar os meses livremente.")



# Criar tabela apenas uma vez

if "tabela" not in st.session_state:

st.session_state.tabela = pd.DataFrame({

"Mês": ["", "", "", "", "", ""],

"Nota Consumidor": [None]*6,

"Total Avaliações": [None]*6,

"Total Solução": [None]*6,

"Total Voltaria": [None]*6

})



st.subheader("📝 Dados")



df = st.data_editor(

st.session_state.tabela,

num_rows="fixed",

use_container_width=True,

column_config={

"Mês": st.column_config.TextColumn("Mês"),

"Nota Consumidor": st.column_config.NumberColumn("Nota", format="%.2f"),

"Total Avaliações": st.column_config.NumberColumn("Avaliações"),

"Total Solução": st.column_config.NumberColumn("Soluções"),

"Total Voltaria": st.column_config.NumberColumn("Voltariam")

}

)



# salvar alterações

st.session_state.tabela = df



# considerar apenas linhas preenchidas

df_validos = df.dropna(subset=["Nota Consumidor"])



if len(df_validos) > 0:



# média simples das notas

media_notas = df_validos["Nota Consumidor"].mean()



# totais

total_av = df_validos["Total Avaliações"].fillna(0).sum()

total_sol = df_validos["Total Solução"].fillna(0).sum()

total_vol = df_validos["Total Voltaria"].fillna(0).sum()



perc_sol = (total_sol / total_av)*100 if total_av > 0 else 0

perc_vol = (total_vol / total_av)*100 if total_av > 0 else 0



st.divider()

st.subheader("📊 Resultado")



col1, col2, col3 = st.columns(3)



col1.metric("Média das Notas", f"{media_notas:.2f}")

col2.metric("% Solução", f"{perc_sol:.1f}%")

col3.metric("% Voltaria", f"{perc_vol:.1f}%")



else:

st.info("Preencha as notas para calcular a média.")
