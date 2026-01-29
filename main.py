import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

# Configuração da página
st.set_page_config(page_title="Dashboard Combustível v3", layout="wide")

# Link da Planilha Google
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
SHEET_NAME = 'Programação'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(SHEET_NAME)}'

def tratar_valor(valor):
    if pd.isna(valor): return 0
    s = str(valor).replace('R$', '').replace('Lts', '').replace('.', '').replace(',', '.').strip()
    try: return float(s)
    except: return 0

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(url)
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

try:
    data = load_data()
    
    st.title("🚢 Relatório de Combustível e Ciclos")
    st.markdown("---")

    # --- SEÇÃO 1: GRÁFICOS POR EMPURRADOR ---
    st.header("⛽ Consumo por Empurrador")
    # Filtra as linhas da primeira tabela (coluna EM)
    df_em = data[['EM', 'TT LITROS', 'TT REIAS']].dropna(subset=['EM']).copy()
    df_em['LITROS'] = df_em['TT LITROS'].apply(tratar_valor)
    df_em['REAIS'] = df_em['TT REIAS'].apply(tratar_valor)
    df_em = df_em[df_em['LITROS'] > 0] # Remove linhas vazias

    c1, c2 = st.columns(2)
    with c1:
        fig_bar = px.bar(df_em, x='EM', y='LITROS', title="Volume (Litros) por Unidade",
                         color='LITROS', color_continuous_scale='Blues', text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with c2:
        fig_pie = px.pie(df_em, values='REAIS', names='EM', hole=0.4,
                         title="% Custo por Empurrador")
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- SEÇÃO 2: GRÁFICOS POR CICLO ---
    st.header("📅 Ciclo de Fevereiro")
    # Filtra as linhas da segunda tabela (coluna CICLO)
    df_ciclo = data[['CICLO', 'TT LITROS.1', 'TT REAIS.1']].dropna(subset=['CICLO']).copy()
    df_ciclo.columns = ['CICLO', 'LITROS', 'REAIS']
    df_ciclo['LITROS'] = df_ciclo['LITROS'].apply(tratar_valor)
    df_ciclo['REAIS'] = df_ciclo['REAIS'].apply(tratar_valor)

    c3, c4 = st.columns(2)
    with c3:
        # Gráfico de Tendência (Linha)
        fig_trend = px.line(df_ciclo, x='CICLO', y='REAIS', markers=True, 
                            title="Tendência de Valores por Ciclo (R$)", line_shape="spline")
        fig_trend.update_traces(line_color='#FF4B4B', line_width=4)
        st.plotly_chart(fig_trend, use_container_width=True)

    with c4:
        # Gráfico de Barras de Ciclo
        fig_ciclo_bar = px.bar(df_ciclo, x='CICLO', y='LITROS', title="Volume (Litros) por Ciclo",
                               color='CICLO', text_auto='.2s')
        st.plotly_chart(fig_ciclo_bar, use_container_width=True)

except Exception as e:
    st.error("Erro ao carregar gráficos. Verifique os nomes das colunas na planilha.")
    st.write(e)
