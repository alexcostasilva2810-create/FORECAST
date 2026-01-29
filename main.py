import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import quote

# Configuração da página e Estilo Visual (Fundo Azul Escuro e Letras 45px)
st.set_page_config(page_title="Dashboard Combustível PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #001f3f; } /* Azul Escuro */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 { 
        color: white !important; 
        font-size: 45px !important; 
        font-family: 'Arial Black', sans-serif;
    }
    /* Ajuste para que os valores dos gráficos não sumam com o tamanho da fonte */
    .plotly-graph-div { font-size: 14px !important; } 
    </style>
    """, unsafe_allow_html=True)

# URL da Planilha Google
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote("Programação")}'

def limpar(v):
    if pd.isna(v): return 0
    s = str(v).replace('R$', '').replace('Lts', '').replace('.', '').replace(',', '.').strip()
    try: return float(s)
    except: return 0

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(url, header=None)
    # Tabela Empurradores (Colunas A, B, C)
    emp = df.iloc[2:12, [0, 1, 2]].copy()
    emp.columns = ['EM', 'LITROS', 'REAIS']
    # Tabela Ciclo Fevereiro (Colunas F, G, H, I, J das linhas 2 e 3)
    cic_lits = df.iloc[2, 5:9].apply(limpar).tolist() # Volume
    cic_reais = df.iloc[3, 5:9].apply(limpar).tolist() # Contábil
    cic_nomes = ['Ciclo 1', 'Ciclo 2', 'Ciclo 3', 'Ciclo 4']
    
    emp['LITROS'] = emp['LITROS'].apply(limpar)
    emp['REAIS'] = emp['REAIS'].apply(limpar)
    
    return emp, pd.DataFrame({'CICLO': cic_nomes, 'LITROS': cic_lits, 'REAIS': cic_reais})

try:
    df_em, df_cic = load_data()

    st.write("⛽ CONSUMO POR EMPURRADOR")

    # 1. Gráfico Misto: Barras (Litros) + Linha (Custo)
    fig1 = go.Figure()
    # Adiciona Barras para Litros
    fig1.add_trace(go.Bar(x=df_em['EM'], y=df_em['LITROS'], name='Litros', 
                          marker_color='cyan', text=df_em['LITROS'], textposition='auto'))
    # Adiciona Linha para Custo (TT REIAS)
    fig1.add_trace(go.Scatter(x=df_em['EM'], y=df_em['REAIS'], name='Custo (R$)', 
                              line=dict(color='yellow', width=6), mode='lines+markers'))
    
    fig1.update_layout(template="plotly_dark", paper_bgcolor='#001f3f', plot_bgcolor='#001f3f',
                      height=700, showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    st.write("📅 PREVISTO: CICLO DE FEVEREIRO")

    col_a, col_b = st.columns(2)

    with col_a:
        # 2. Gráfico de Pizza para Volume (Litros)
        st.write("🍕 Volume (Litros)")
        fig_pie = px.pie(df_cic, values='LITROS', names='CICLO', 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='#001f3f')
        fig_pie.update_traces(textinfo='percent+label', textfont_size=20)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        # 3. Gráfico de Linha para Contábil (R$)
        st.write("📈 Contábil (R$)")
        fig_line = px.line(df_cic, x='CICLO', y='REAIS', markers=True)
        fig_line.update_traces(line=dict(color='#00ff00', width=8), marker=dict(size=15))
        fig_line.update_layout(template="plotly_dark", paper_bgcolor='#001f3f', plot_bgcolor='#001f3f')
        st.plotly_chart(fig_line, use_container_width=True)

except Exception as e:
    st.error("ERRO AO CARREGAR OS DADOS")
    st.write(f"Detalhes: {e}")
