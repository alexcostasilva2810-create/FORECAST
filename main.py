import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para ocupar a tela inteira
st.set_page_config(page_title="Dashboard Consumo - AQ 084", layout="wide")

# --- CONFIGURAÇÃO DA FONTE DE DADOS ---
# ID extraído do link que você enviou
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
# Aba onde estão os dados de consumo por unidade (Cumaru, Jatobá, etc.)
SHEET_NAME = 'Programação' 

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

@st.cache_data(ttl=600) # Atualiza os dados a cada 10 minutos
def load_data():
    # Lendo os dados e tratando possíveis problemas de formatação
    df = pd.read_csv(url)
    # Limpeza básica: remove linhas totalmente vazias
    df = df.dropna(subset=['EM', 'TT LITROS'])
    return df

# --- INTERFACE DO DASHBOARD ---
st.title("⛽ Painel de Controle de Combustível")
st.markdown(f"**Fonte:** Planilha Google - Aba: `{SHEET_NAME}`")

try:
    df = load_data()

    # --- MÉTRICAS PRINCIPAIS (KPIs) ---
    total_litros = df['TT LITROS'].sum()
    # Ajuste de conversão para Real (considerando que na planilha pode vir como string)
    if df['TT REAIS'].dtype == object:
        df['TT REAIS'] = df['TT REAIS'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)
    
    total_reais = df['TT REAIS'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Volume Total", f"{total_litros:,.2f} L".replace(",", "v").replace(".", ",").replace("v", "."))
    col2.metric("Investimento Total", f"R$ {total_reais:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    col3.metric("Unidades Atendidas", len(df['EM'].unique()))

    st.divider()

    # --- GRÁFICOS ---
    col_dir, col_esq = st.columns(2)

    with col_dir:
        st.subheader("Consumo por Unidade (Litros)")
        fig_bar = px.bar(
            df, 
            x='EM', 
            y='TT LITROS', 
            color='TT LITROS',
            color_continuous_scale='Blues',
            text_auto='.2s'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_esq:
        st.subheader("Distribuição de Custos (R$)")
        fig_pie = px.pie(
            df, 
            values='TT REAIS', 
            names='EM', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABELA DE DADOS ---
    st.subheader("📋 Detalhamento dos Dados")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Ops! Não consegui ler os dados.")
    st.info("Verifique se a planilha está compartilhada como 'Qualquer pessoa com o link' no Google Sheets.")
    st.exception(e)
