import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

st.set_page_config(page_title="Dashboard Consumo", layout="wide")

# Configurações da Planilha
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
SHEET_NAME = 'Programação'
# O segredo está aqui: tratar o nome da aba para evitar o erro de 'ascii'
encoded_sheet_name = quote(SHEET_NAME)

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}'

@st.cache_data(ttl=600)
def load_data():
    # Forçamos o encoding utf-8 para ler acentos corretamente
    df = pd.read_csv(url, encoding='utf-8')
    return df

st.title("⛽ Painel de Controle de Combustível")

try:
    df = load_data()
    st.success("Dados carregados com sucesso!")
    
    # Exibir os dados para testar
    st.dataframe(df.head())
    
    # Gráfico simples de teste
    if 'EM' in df.columns and 'TT LITROS' in df.columns:
        fig = px.bar(df, x='EM', y='TT LITROS', title="Consumo por Unidade")
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Erro ao carregar dados. Verifique se a planilha está aberta para 'Qualquer pessoa com o link'.")
    st.write(f"Detalhes do erro: {e}")
