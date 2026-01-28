import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

# Configuração da Página
st.set_page_config(page_title="Dashboard de Combustível", layout="wide")

# Configurações do Google Sheets
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
SHEET_NAME = 'Programação'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(SHEET_NAME)}'

@st.cache_data(ttl=300)
def load_data():
    # Carregamento forçando UTF-8 para evitar erro de 'ascii'
    df = pd.read_csv(url, encoding='utf-8')
    
    # Tratamento de dados: convertendo valores financeiros
    if 'TT REAIS' in df.columns:
        df['TT REAIS'] = df['TT REAIS'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)
    
    # Removendo linhas vazias
    df = df.dropna(subset=['EMPURRADOR', 'TT LITROS'])
    return df

try:
    df = load_data()

    st.title("⛽ Gestão de Combustível por Ciclo")
    st.markdown("---")

    # --- KPIs NO TOPO ---
    c1, c2, c3 = st.columns(3)
    total_litros = df['TT LITROS'].sum()
    total_reais = df['TT REAIS'].sum()
    
    c1.metric("Total de Litros", f"{total_litros:,.0f} L".replace(',', '.'))
    c2.metric("Investimento Total", f"R$ {total_reais:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.'))
    c3.metric("Média por Ciclo", f"{df['TT LITROS'].mean():,.0f} L".replace(',', '.'))

    st.markdown("### 📊 Análise Visual")
    
    col_dir, col_esq = st.columns(2)

    with col_dir:
        # GRAFICO DE BARRAS: Consumo por Empurrador
        st.subheader("Consumo por Empurrador (Barras)")
        fig_bar = px.bar(df, x='EMPURRADOR', y='TT LITROS', color='EMPURRADOR',
                         text_auto='.2s', template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_esq:
        # GRAFICO DE PIZZA: % por Empurrador
        st.subheader("Distribuição % de Custos")
        fig_pie = px.pie(df, values='TT REAIS', names='EMPURRADOR', hole=0.4)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    
    # GRAFICO DE TENDÊNCIA: Mapa de valores por Ciclo
    st.subheader("📈 Mapa de Tendência de Valores por Ciclo")
    if 'CICLO' in df.columns:
        # Agrupando por ciclo para ver a tendência
        df_ciclo = df.groupby('CICLO')['TT REAIS'].sum().reset_index()
        fig_trend = px.line(df_ciclo, x='CICLO', y='TT REAIS', markers=True, 
                            line_shape="spline", title="Evolução Financeira por Ciclo")
        fig_trend.update_traces(line_color='#FF4B4B', line_width=4)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("Coluna 'CICLO' não encontrada. Exibindo tendência geral.")
        fig_trend = px.line(df, y='TT REAIS', markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

except Exception as e:
    st.error("Erro ao conectar com a planilha.")
    st.info("Verifique se a planilha está como 'Qualquer pessoa com o link'.")
    st.code(f"Detalhes: {e}")
