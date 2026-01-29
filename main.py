import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. ESTILO DE ALTO IMPACTO (FUNDO AZUL PROFUNDO E FONTES 45PX)
st.set_page_config(page_title="Forecast Fevereiro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #030a1c !important; }
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, div { 
        color: #FFFFFF !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-title { font-size: 60px !important; font-weight: 800; color: #00d4ff; text-align: center; margin-bottom: 20px; }
    .sub-title { font-size: 45px !important; font-weight: 700; border-left: 10px solid #00d4ff; padding-left: 20px; margin: 40px 0; }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO GIGANTE
st.markdown('<p class="main-title">FORECAST DE CONSUMO PARA FEVEREIRO</p>', unsafe_allow_html=True)

# 3. DADOS EXATOS
dados = {
    'EM': ['CUMARU', 'IPE', 'JATOBA', 'AROEIRA', 'SAMAUAMA', 'ANGICO', 'LUIZ FELIPE', 'JACARANDA', 'CAJERANA', 'QUARUBA'],
    'LITROS': [81628.8, 45777.6, 37804.8, 37804.8, 35706.0, 33079.2, 28934.4, 19588.8, 19588.8, 8395.2],
    'REAIS': [485115.84, 241005.60, 198002.64, 198002.64, 186028.26, 191859.36, 167819.52, 115643.88, 115699.85, 60445.44],
    'CICLO': ['CICLO 1', 'CICLO 2', 'CICLO 3', 'CICLO 4', '', '', '', '', '', ''],
    'VOL_CICLO': [140950, 132488, 13992, 60878, 0, 0, 0, 0, 0, 0],
    'RS_CICLO': [818763.26, 724684.62, 86540.52, 329634.62, 0, 0, 0, 0, 0, 0]
}
df = pd.DataFrame(dados)

# --- GRÁFICO 1: CONSUMO POR EMPURRADOR (BARRAS + LINHA) ---
st.markdown('<p class="sub-title">⚓ CONSUMO POR EMPURRADOR (LITROS vs R$)</p>', unsafe_allow_html=True)
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=df['EM'], y=df['LITROS'], name='LITROS', marker_color='#00f2ff', text=df['LITROS'], textposition='outside'))
fig1.add_trace(go.Scatter(x=df['EM'], y=df['REAIS'], name='CUSTO CONTÁBIL', line=dict(color='#fbff00', width=10), mode='lines+markers'))

fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=600, 
                  font=dict(size=18), margin=dict(t=50))
st.plotly_chart(fig1, use_container_width=True)

# --- LINHA 2: CICLO DE FEVEREIRO ---
st.markdown('<p class="sub-title">📅 PREVISTO CICLO DE FEVEREIRO</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

df_c = df.head(4) # Pega apenas os 4 ciclos

with c1:
    fig2 = px.pie(df_c, values='VOL_CICLO', names='CICLO', hole=0.5, title="VOLUME POR CICLO (Lts)")
    fig2.update_traces(textinfo='percent+label', marker=dict(colors=['#00d4ff', '#0055ff', '#00ffaa', '#ff0055']))
    fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    fig3 = px.line(df_c, x='CICLO', y='RS_CICLO', title="TENDÊNCIA CONTÁBIL (R$)")
    fig3.update_traces(line=dict(color='#00ff44', width=12), marker=dict(size=20, color="white"))
    fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
    st.plotly_chart(fig3, use_container_width=True)
    
