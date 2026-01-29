import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

st.set_page_config(page_title="Dashboard Combustível Final", layout="wide")

# Link da Planilha
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
SHEET_NAME = 'Programação'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(SHEET_NAME)}'

def converter_numero(valor):
    if pd.isna(valor): return 0
    # Limpa R$, pontos de milhar e troca vírgula por ponto
    s = str(valor).replace('R$', '').replace('Lts', '').replace('.', '').replace(',', '.').strip()
    try: return float(s)
    except: return 0

@st.cache_data(ttl=60)
def load_data():
    # Lê a planilha sem cabeçalho para não dar erro de nome de coluna
    df = pd.read_csv(url, header=None)
    return df

try:
    df = load_data()
    
    st.title("📊 Painel de Controle de Combustível")
    st.markdown("---")

    # --- TABELA 1: EMPURRADORES (Colunas A, B, C -> 0, 1, 2) ---
    # Pegamos da linha 3 em diante (onde começam os dados após o cabeçalho)
    df_em = df.iloc[2:12, [0, 1, 2]].copy() 
    df_em.columns = ['NOME', 'LITROS', 'REAIS']
    df_em['LITROS'] = df_em['LITROS'].apply(converter_numero)
    df_em['REAIS'] = df_em['REAIS'].apply(converter_numero)
    df_em = df_em[df_em['LITROS'] > 0]

    # --- TABELA 2: CICLOS (Colunas F, G, H -> 5, 6, 7) ---
    df_ciclo = df.iloc[2:6, [5, 6, 7]].copy()
    df_ciclo.columns = ['CICLO', 'LITROS', 'REAIS']
    df_ciclo['LITROS'] = df_ciclo['LITROS'].apply(converter_numero)
    df_ciclo['REAIS'] = df_ciclo['REAIS'].apply(converter_numero)

    # --- DISPLAY DOS GRÁFICOS ---
    
    st.header("🚢 Consumo por Empurrador")
    col1, col2 = st.columns(2)
    with col1:
        # Gráfico de Barras
        fig_bar = px.bar(df_em, x='NOME', y='LITROS', color='NOME', 
                         title="Volume (Lts) por Unidade", text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        # Gráfico de Pizza com %
        fig_pie = px.pie(df_em, values='REAIS', names='NOME', hole=0.4, 
                         title="% Custo Financeiro")
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    
    st.header("📅 Ciclo de Fevereiro")
    col3, col4 = st.columns(2)
    with col3:
        # Gráfico de Tendência (Linha)
        fig_trend = px.line(df_ciclo, x='CICLO', y='REAIS', markers=True, 
                            title="Tendência de Valores (R$)", line_shape="spline")
        fig_trend.update_traces(line_color='#FF4B4B', line_width=4)
        st.plotly_chart(fig_trend, use_container_width=True)
    with col4:
        # Gráfico de Barras Ciclo
        fig_ciclo_bar = px.bar(df_ciclo, x='CICLO', y='LITROS', color='CICLO', 
                               title="Volume por Ciclo (Lts)", text_auto='.2s')
        st.plotly_chart(fig_ciclo_bar, use_container_width=True)

except Exception as e:
    st.error("Erro na leitura das posições da planilha.")
    st.write(f"Detalhe: {e}")
    # Mostra a planilha bruta para a gente debugar se precisar
    st.write("Dados Brutos lidos:", df.head(10))
