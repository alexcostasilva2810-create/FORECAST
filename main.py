import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. ESTILO VISUAL: FUNDO AZUL ESCURO + LETRAS GIGANTES (45PX)
st.set_page_config(page_title="Forecast Fevereiro", layout="wide")

st.markdown("""
    <style>
    /* Fundo azul escuro em toda a tela */
    .main { background-color: #001f3f !important; }
    
    /* Configuração da Fonte 45px em Branco */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, div { 
        color: #FFFFFF !important; 
        font-size: 45px !important; 
        font-family: 'Arial Black', sans-serif;
        font-weight: bold;
    }
    
    /* Ajuste para o gráfico não ficar com legenda pequena */
    .legendtext { font-size: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO SOLICITADO
st.write("Forecast de consumo para Fevereiro")
st.markdown("---")

# 3. DADOS DO CONSUMO POR EMPURRADOR
dados = {
    'EM': ['CUMARU', 'IPE', 'JATOBA', 'AROEIRA', 'SAMAUAMA', 'ANGICO', 'LUIZ FELIPE', 'JACARANDA', 'CAJERANA', 'QUARUBA'],
    'LITROS': [81628.8, 45777.6, 37804.8, 37804.8, 35706.0, 33079.2, 28934.4, 19588.8, 19588.8, 8395.2],
    'REAIS': [485115.84, 241005.60, 198002.64, 198002.64, 186028.26, 191859.36, 167819.52, 115643.88, 115699.85, 60445.44]
}

df = pd.DataFrame(dados)

# 4. GRÁFICO EXPOSITIVO (BARRAS + LINHA CONTÁBIL)
fig = go.Figure()

# Barras para Litros (Ciano)
fig.add_trace(go.Bar(
    x=df['EM'], 
    y=df['LITROS'], 
    name='LITROS',
    marker_color='#00FFFF', # Ciano
    text=df['LITROS'],
    textposition='outside',
    textfont=dict(size=20, color="white")
))

# Linha para Custo Contábil (Amarelo)
fig.add_trace(go.Scatter(
    x=df['EM'], 
    y=df['REAIS'], 
    name='R$ CONTÁBIL',
    line=dict(color='#FFFF00', width=10), # Amarelo Neon Grosso
    mode='lines+markers',
    marker=dict(size=15)
))

# Ajustes de Layout do Gráfico
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=800,
    showlegend=True,
    legend=dict(font=dict(size=25)),
    xaxis=dict(tickfont=dict(size=20)),
    yaxis=dict(tickfont=dict(size=20), title="Volume / Valor")
)

st.plotly_chart(fig, use_container_width=True)
