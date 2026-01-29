import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import quote

# Configuração da página para o Estilo Dark
st.set_page_config(page_title="Gestão de Frota PRO", layout="wide", initial_sidebar_state="collapsed")

# CSS para forçar o visual Dark e cartões modernos
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    div[data-testid="metric-container"] { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# URL da Planilha
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote("Programação")}'

def limpar(v):
    if pd.isna(v): return 0
    s = str(v).replace('R$', '').replace('Lts', '').replace('.', '').replace(',', '.').strip()
    try: return float(s)
    except: return 0

@st.cache_data(ttl=60)
def load_data():
    # Lê os dados brutos e ignora nomes de colunas problemáticos
    df = pd.read_csv(url, header=None)
    
    # Extração da Tabela de Empurradores (Posições fixas baseadas na sua imagem)
    emp = df.iloc[2:12, [0, 1, 2]].copy()
    emp.columns = ['NOME', 'LITROS', 'REAIS']
    emp['LITROS'] = emp['LITROS'].apply(limpar)
    emp['REAIS'] = emp['REAIS'].apply(limpar)
    
    # Extração da Tabela de Ciclos
    cic = df.iloc[2:6, [5, 6, 7]].copy()
    cic.columns = ['CICLO', 'LITROS', 'REAIS']
    cic['LITROS'] = cic['LITROS'].apply(limpar)
    cic['REAIS'] = cic['REAIS'].apply(limpar)
    
    return emp[emp['LITROS'] > 0], cic

try:
    df_em, df_ciclo = load_data()

    # --- HEADER ---
    st.title("🚀 Dashboard de Operações Marítimas")
    
    # --- KPIs (Cartões de Topo) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Litros", f"{df_em['LITROS'].sum():,.0f} L")
    c2.metric("Investimento", f"R$ {df_em['REAIS'].sum():,.2f}")
    c3.metric("Média/Empurrador", f"R$ {df_em['REAIS'].mean():,.2f}")
    c4.metric("Eficiência", "94.2%")

    st.markdown("---")

    # --- LINHA 1 DE GRÁFICOS ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Gráfico de Tendência de Ciclos (Igual ao da imagem)
        st.subheader("📈 Mapa de Tendência Financeira por Ciclo")
        fig_line = px.line(df_ciclo, x='CICLO', y='REAIS', markers=True, line_shape='spline')
        fig_line.update_traces(line_color='#58a6ff', line_width=4, fill='tozeroy') # Efeito de preenchimento
        fig_line.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        # Donut Chart de Distribuição
        st.subheader("🎯 Participação no Custo")
        fig_donut = px.pie(df_em, values='REAIS', names='NOME', hole=0.6)
        fig_donut.update_traces(textinfo='percent')
        fig_donut.update_layout(template="plotly_dark", showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, use_container_width=True)

    # --- LINHA 2 DE GRÁFICOS ---
    col_b1, col_b2 = st.columns(2)

    with col_b1:
        st.subheader("📊 Consumo de Combustível (Litros)")
        fig_bar = px.bar(df_em, x='NOME', y='LITROS', color='LITROS', color_continuous_scale='Viridis')
        fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b2:
        st.subheader("📋 Resumo de Dados")
        st.dataframe(df_em.style.format({'LITROS': '{:,.0f}', 'REAIS': 'R$ {:,.2f}'}), use_container_width=True)

except Exception as e:
    st.error("Erro na sincronização dos dados.")
    st.write(f"Detalhes: {e}")
