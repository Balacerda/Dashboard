import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Título do Dashboard
st.title("Dashboard de Dispersão de Carteira")
st.write("Monitoramento da dispersão da carteira de corretores de seguros.")

# Upload de Arquivo
uploaded_file = st.file_uploader("Faça o upload do arquivo Excel", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Visualização dos Dados:")
    st.dataframe(df.head())

    # Seleção de Filtros
    corretores = df['Corretor'].unique()
    corretor_selecionado = st.selectbox("Selecione o Corretor", corretores)

    # Filtrar dados
    df_filtrado = df[df['Corretor'] == corretor_selecionado]

    # Gráfico de Dispersão
    st.write("### Dispersão de Carteira")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_filtrado, x='Seguradora', y='% Carteira', hue='Risco', size='% Carteira', sizes=(20, 200), ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Seguradoras")
    plt.ylabel("% da Carteira")
    plt.title(f"Dispersão da Carteira do Corretor {corretor_selecionado}")
    st.pyplot(fig)

    # Estatísticas Gerais
    st.write("### Estatísticas Gerais")
    st.write(df_filtrado.describe())
    
    # Alertas de Incumprimento
    st.write("### Alertas de Incumprimento")
    limite_concentracao = 50  # Ajustável conforme regra de negócio
    corretores_em_risco = df[df['% Carteira'] > limite_concentracao]
    if not corretores_em_risco.empty:
        st.warning("Corretores com alta concentração de carteira identificados!")
        st.dataframe(corretores_em_risco[['Corretor', 'Seguradora', '% Carteira']])
    else:
        st.success("Nenhum corretor em risco identificado.")
