import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

# Configuração visual
st.set_page_config(page_title="Dashboard de Combustível - PRO", layout="wide")

# Estilização personalizada
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# Configurações da Planilha
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
SHEET_NAME = 'Programação'
encoded_name = quote(SHEET_NAME)
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}'

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(url)
    # Limpeza de colunas vazias e tratamento de nomes
    df = df.dropna(subset=['EMPURRADOR', 'TT LITROS'])
    # Converter TT REAIS para numérico (remove R$ e ajusta vírgula)
    if df['TT REAIS'].dtype == object:
        df['TT REAIS'] = df['TT REAIS'].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)
    return df

try:
    df = load_data()

    st.title("📊 Gestão Inteligente de Combustível")
    st.markdown("---")

    # --- MÉTRICAS DE TOPO ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Litros", f"{df['TT LITROS'].sum():,.0f} L".replace(',', '.'))
    c2.metric("Total Investido", f"R$ {df['TT REAIS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    c3.metric("Média por Empurrador", f"{df['TT LITROS'].mean():,.0f} L".replace(',', '.'))

    st.markdown("### 📈 Análise de Consumo")
    
    col_a, col_b = st.columns(2)

    with col_a:
        # Gráfico de Barras: Consumo por Empurrador
        st.subheader("Volume por Empurrador (Litros)")
        fig_bar = px.bar(df, x='EMPURRADOR', y='TT LITROS', color='EMPURRADOR', 
                         text_auto='.2s', template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        # Gráfico de Pizza: Porcentagem por Empurrador
        st.subheader("% de Gasto por Empurrador")
        fig_pie = px.pie(df, values='TT REAIS', names='EMPURRADOR', hole=0.4,
                         template="plotly_white")
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    
    col_c, col_d = st.columns(2)

    with col_c:
        # Gráfico de Tendência (Linha)
        st.subheader("Tendência de Valores por Lançamento")
        fig_line = px.line(df, y='TT REAIS', markers=True, 
                           title="Evolução do Custo (R$)", line_shape="spline")
        fig_line.update_traces(line_color='#ef553b')
        st.plotly_chart(fig_line, use_container_width=True)

    with col_d:
        # Gráfico de Barras por Ciclo
        if 'CICLO' in df.columns:
            st.subheader("Consumo por Ciclo")
            fig_ciclo = px.bar(df, x='CICLO', y='TT LITROS', color='CICLO', barmode='group')
            st.plotly_chart(fig_ciclo, use_container_width=True)
        else:
            st.info("Coluna 'CICLO' não encontrada para gerar o gráfico específico.")

    # Tabela detalhada
    with st.expander("Visualizar Dados Completos"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Erro ao processar os dados. Verifique o compartilhamento da planilha.")
    st.write(f"Dica: O nome da aba deve ser exatamente '{SHEET_NAME}'")
