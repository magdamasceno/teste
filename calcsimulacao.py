import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora 6 Meses", layout="wide")

st.title("📊 Calculadora de Indicadores - Últimos 6 Meses")

st.write("Preencha os dados mensais para calcular automaticamente as médias dos últimos 6 meses.")

# Estrutura da tabela
colunas = [
    "Mês",
    "Nota Consumidor",
    "Total Avaliações",
    "Total Solução",
    "Total Voltaria"
]

# Tabela inicial com 6 linhas
dados_iniciais = pd.DataFrame({
    "Mês": ["", "", "", "", "", ""],
    "Nota Consumidor": [0.0]*6,
    "Total Avaliações": [0]*6,
    "Total Solução": [0]*6,
    "Total Voltaria": [0]*6
})

st.subheader("📝 Inserção de Dados")

df = st.data_editor(
    dados_iniciais,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Mês": st.column_config.TextColumn("Mês"),
        "Nota Consumidor": st.column_config.NumberColumn("Nota Consumidor", format="%.2f"),
        "Total Avaliações": st.column_config.NumberColumn("Total Avaliações"),
        "Total Solução": st.column_config.NumberColumn("Total Solução"),
        "Total Voltaria": st.column_config.NumberColumn("Total Voltaria")
    }
)

# Remover linhas vazias
df_validos = df[df["Total Avaliações"] > 0]

if len(df_validos) > 0:

    df_calc = df_validos.copy()

    # Cálculo das porcentagens mensais
    df_calc["% Solução"] = (df_calc["Total Solução"] / df_calc["Total Avaliações"]) * 100
    df_calc["% Voltaria"] = (df_calc["Total Voltaria"] / df_calc["Total Avaliações"]) * 100

    st.subheader("📈 Indicadores por Mês")

    st.dataframe(
        df_calc.style.format({
            "Nota Consumidor": "{:.2f}",
            "% Solução": "{:.1f}%",
            "% Voltaria": "{:.1f}%"
        }),
        use_container_width=True
    )

    # Totais gerais
    total_avaliacoes = df_calc["Total Avaliações"].sum()
    total_solucoes = df_calc["Total Solução"].sum()
    total_voltaria = df_calc["Total Voltaria"].sum()

    # Média das notas (igual Excel)
    media_notas = df_calc["Nota Consumidor"].mean()

    # Percentuais gerais
    perc_solucao = (total_solucoes / total_avaliacoes) * 100
    perc_voltaria = (total_voltaria / total_avaliacoes) * 100

    st.subheader("📊 Resultado Geral (6 meses)")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Média das Notas",
        f"{media_notas:.2f}"
    )

    col2.metric(
        "% Solução",
        f"{perc_solucao:.1f}%"
    )

    col3.metric(
        "% Voltaria",
        f"{perc_voltaria:.1f}%"
    )

else:

    st.info("Preencha os dados para visualizar os resultados.")
