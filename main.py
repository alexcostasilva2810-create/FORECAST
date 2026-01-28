import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Consumo AQ 084", layout="wide")

# Título
st.title("📊 Relatório de Consumo de Combustível - Atualizado")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("dados_em.csv")
    return df

df = load_data()

# --- KPIs (Métricas Principais) ---
total_litros = df["TT_LITROS"].sum()
total_reais = df["TT_REAIS"].sum()

col1, col2 = st.columns(2)
col1.metric("Total de Litros", f"{total_litros:,.2f} L".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Total em Reais", f"R$ {total_reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- Gráficos ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Consumo por Unidade (Litros)")
    fig_litros = px.bar(df, x="EM", y="TT_LITROS", text_auto='.2s',
                        color="TT_LITROS", color_continuous_scale="Viridis")
    st.plotly_chart(fig_litros, use_container_width=True)

with col_graf2:
    st.subheader("Custo por Unidade (Reais)")
    fig_reais = px.pie(df, values="TT_REAIS", names="EM", hole=0.4)
    st.plotly_chart(fig_reais, use_container_width=True)

# Exibir Tabela de Dados
st.subheader("Visualização dos Dados Brutos")
st.dataframe(df, use_container_width=True)
