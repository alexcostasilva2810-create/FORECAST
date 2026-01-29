import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

st.set_page_config(page_title="Dashboard Combustível", layout="wide")

# Configurações da Planilha
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
SHEET_NAME = 'Programação'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(SHEET_NAME)}'

def limpar_moeda(valor):
    if isinstance(valor, str):
        return valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
    return valor

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(url)
    # Limpeza de nomes de colunas
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Tratamento numérico
    for col in ['TT LITROS', 'TT REAIS']:
        if col in df.columns:
            df[col] = df[col].apply(limpar_moeda)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

try:
    df_raw = load_data()

    st.title("🚢 Monitoramento de Frota e Ciclos")
    st.markdown("---")

    # --- SEÇÃO 1: ANÁLISE POR EMPURRADOR ---
    st.header("1️⃣ Consumo por Empurrador (EM)")
    # Filtramos apenas as linhas que têm nome de Empurrador (coluna EM)
    df_em = df_raw.dropna(subset=['EM']).iloc[:10] # Pega as 10 unidades da imagem

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Volume Total (Litros)")
        fig_bar = px.bar(df_em, x='EM', y='TT LITROS', color='EM', 
                         text_auto='.2s', title="Litros por Unidade")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("% Distribuição de Custos")
        fig_pie = px.pie(df_em, values='TT REAIS', names='EM', hole=0.4)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- SEÇÃO 2: ANÁLISE POR CICLO ---
    st.header("2️⃣ Ciclo de Fevereiro")
    # Filtramos a parte da tabela que fala de Ciclo
    df_ciclo = df_raw.dropna(subset=['CICLO']).iloc[:4] # Ciclos 1 a 4

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Tendência de Gasto por Ciclo")
        fig_trend = px.line(df_ciclo, x='CICLO', y='TT REAIS', markers=True, 
                            line_shape="spline", title="Evolução Financeira")
        fig_trend.update_traces(line_color='#FF4B4B', line_width=4)
        st.plotly_chart(fig_trend, use_container_width=True)

    with col4:
        st.subheader("Consumo de Litros por Ciclo")
        fig_ciclo_bar = px.bar(df_ciclo, x='CICLO', y='TT LITROS', 
                               color='CICLO', text_auto='.2s')
        st.plotly_chart(fig_ciclo_bar, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao processar: {e}")
    st.info("Verifique se as colunas na planilha são: EM, TT LITROS, TT REAIS e CICLO.")
