# https://rlfhcsydmtre5rvsbvrppa.streamlit.app/
# https://github.com/lucascxr70/StreamlitClass.git

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Definir o estilo escuro
plt.style.use('dark_background')

# Caminhos para os arquivos CSV
hapvida_path = os.path.join(os.getcwd(), 'resources', 'RECLAMEAQUI_HAPVIDA.csv')
ibyte_path = os.path.join(os.getcwd(), 'resources', 'RECLAMEAQUI_IBYTE.csv')
nagem_path = os.path.join(os.getcwd(), 'resources', 'RECLAMEAQUI_NAGEM.csv')

# Carregar os datasets
hapvida = pd.read_csv(hapvida_path)
ibyte = pd.read_csv(ibyte_path)
nagem = pd.read_csv(nagem_path)

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

# Gráfico de série temporal do número de reclamações
st.subheader("Série Temporal do Número de Reclamações")

# Agrupar as reclamações por mês e contar o número de reclamações por mês
reclamacoes_por_mes = df_filtrado.groupby(df_filtrado['DATA'].dt.to_period('M'))['empresa'].count()

# Ajustar a visualização do gráfico com Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))

# Plotar a série temporal
ax.plot(reclamacoes_por_mes.index.to_timestamp(), reclamacoes_por_mes, color='lightblue', linewidth=2)

# Ajustar os rótulos do eixo X para exibir meses de cada ano (jan 2022, fev 2022, etc.)
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=3))  # Mostrar um mês a cada 3 para espaçamento

# Rotacionar os rótulos do eixo X para melhor visualização
plt.xticks(rotation=45)

# Título e rótulos dos eixos
ax.set_title("Série Temporal do Número de Reclamações", fontsize=16)
ax.set_xlabel("Mês e Ano", fontsize=12)
ax.set_ylabel("Número de Reclamações", fontsize=12)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Gráfico de frequência de reclamações por estado (usando Matplotlib)
st.subheader("Frequência de Reclamações por Estado")
df_filtrado['ESTADO'] = df_filtrado['LOCAL'].str.split(' - ').str[-1]  # Extrair o estado da coluna LOCAL
reclamacoes_por_estado = df_filtrado['ESTADO'].value_counts()

# Criar o gráfico de barras com a cor 'lightblue'
fig, ax = plt.subplots()
reclamacoes_por_estado.plot(kind='bar', ax=ax, color='lightblue')
ax.set_xlabel("Estado", fontsize=12)
ax.set_ylabel("Número de Reclamações", fontsize=12)
ax.set_title("Frequência de Reclamações por Estado", fontsize=14)
st.pyplot(fig)

# Gráfico de frequência de status das reclamações (usando Matplotlib)
st.subheader("Frequência de Cada Tipo de Status")
status_frequencia = df_filtrado['STATUS'].value_counts()

# Criar o gráfico de barras com a cor 'lightblue'
fig, ax = plt.subplots()
status_frequencia.plot(kind='bar', ax=ax, color='lightblue')
ax.set_xlabel("Status", fontsize=12)
ax.set_ylabel("Número de Reclamações", fontsize=12)
ax.set_title("Frequência de Cada Tipo de Status", fontsize=14)
st.pyplot(fig)

# Gráfico de distribuição do tamanho do texto (coluna DESCRICAO) (usando Matplotlib e Seaborn)
st.subheader("Distribuição do Tamanho do Texto (Descrição)")
df_filtrado['tamanho_texto'] = df_filtrado['DESCRICAO'].str.len()

fig, ax = plt.subplots()
sns.histplot(df_filtrado['tamanho_texto'], bins=30, ax=ax, color='lightblue')

# Ajustando os rótulos dos eixos X e Y
ax.set_xlabel("Comprimento do Texto (Caracteres)", fontsize=12)
ax.set_ylabel("Contagem de Reclamações", fontsize=12)

# Ajustando o título do gráfico
ax.set_title("Distribuição do Comprimento das Descrições", fontsize=14)

# Exibir o gráfico no Streamlit
st.pyplot(fig)
