import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Carregar os datasets
hapvida = pd.read_csv(r'..\resources\RECLAMEAQUI_HAPVIDA.csv')
ibyte = pd.read_csv(r'..\resources\RECLAMEAQUI_IBYTE.csv')
nagem = pd.read_csv(r'..\resources\RECLAMEAQUI_NAGEM.csv')

# Adicionar uma coluna para identificar a empresa
hapvida['empresa'] = 'Hapvida'
ibyte['empresa'] = 'Ibyte'
nagem['empresa'] = 'Nagem'

# Combinar os datasets
df = pd.concat([hapvida, ibyte, nagem])

# Definir o título do painel
st.title('Painel de Reclamações de Empresas')

# Filtros dinâmicos com seletor múltiplo
empresas_selecionadas = st.multiselect("Selecione a(s) empresa(s)", df['empresa'].unique(), default=df['empresa'].unique())
estados_selecionados = st.multiselect("Selecione o(s) estado(s)", df['LOCAL'].str.split(' - ').str[-1].unique(), default=df['LOCAL'].str.split(' - ').str[-1].unique())
status_selecionados = st.multiselect("Selecione o(s) status", df['STATUS'].unique(), default=df['STATUS'].unique())
tamanho_texto = st.slider("Selecione o tamanho do texto (descrição)", 0, df['DESCRICAO'].str.len().max())


# Converter colunas de data (ANO, MES, DIA) para datetime
df['DATA'] = pd.to_datetime(df[['ANO', 'MES', 'DIA']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d', errors='coerce')

# Aplicar filtros no DataFrame com seletores múltiplos
df_filtrado = df[
    (df['empresa'].isin(empresas_selecionadas)) &
    (df['LOCAL'].str.split(' - ').str[-1].isin(estados_selecionados)) &
    (df['STATUS'].isin(status_selecionados)) &
    (df['DESCRICAO'].str.len() <= tamanho_texto)
]

# # Verificar o conteúdo de 'DATA' no DataFrame filtrado
# st.write(df_filtrado[['DATA', 'empresa', 'DESCRICAO']].head())

# Gráfico de série temporal do número de reclamações por mês
st.subheader("Série Temporal do Número de Reclamações por Mês")

# Agrupar as reclamações por mês e contar o número de reclamações por mês
reclamacoes_por_mes = df_filtrado.groupby(df_filtrado['DATA'].dt.to_period('M'))['empresa'].count()

# Mostrar o gráfico
st.line_chart(reclamacoes_por_mes)

# Gráfico de frequência de reclamações por estado
st.subheader("Frequência de Reclamações por Estado")
df_filtrado['ESTADO'] = df_filtrado['LOCAL'].str.split(' - ').str[-1]  # Extrair o estado da coluna LOCAL
reclamacoes_por_estado = df_filtrado['ESTADO'].value_counts()
st.bar_chart(reclamacoes_por_estado)

# Gráfico de frequência de status das reclamações
st.subheader("Frequência de Cada Tipo de Status")
status_frequencia = df_filtrado['STATUS'].value_counts()
st.bar_chart(status_frequencia)

# Gráfico de distribuição do tamanho do texto (coluna DESCRICAO)
st.subheader("Distribuição do Tamanho do Texto (Descrição)")
df_filtrado['tamanho_texto'] = df_filtrado['DESCRICAO'].str.len()

fig, ax = plt.subplots()
sns.histplot(df_filtrado['tamanho_texto'], bins=30, ax=ax)

# Ajustando os rótulos dos eixos X e Y
ax.set_xlabel("Comprimento do Texto (Caracteres)", fontsize=12)
ax.set_ylabel("Contagem de Reclamações", fontsize=12)

# Ajustando o título do gráfico
ax.set_title("Distribuição do Comprimento das Descrições", fontsize=14)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

