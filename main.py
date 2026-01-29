import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. SETUP DE DESIGN AGRESSIVO (FUNDO AZUL-NEGRO + FONTES 45PX)
st.set_page_config(page_title="FORECAST FEVEREIRO", layout="wide")

# Forçando o visual via CSS para não ter erro de tema branco
st.markdown("""
    <style>
    /* Fundo Escuro Profundo */
    .stApp { background-color: #030a1c !important; }
    
    /* Título Principal 60px Ciano */
    .main-title {
        font-size: 60px !important;
        color: #00f2ff !important;
        text-align: center;
        font-weight: 900;
        text-transform: uppercase;
        padding: 40px;
        border-bottom: 5px solid #00f2ff;
    }

    /* Subtítulos 45px Branco */
    .sub-title {
        font-size: 45px !important;
        color: #ffffff !important;
        font-weight: 800;
        margin-top: 50px;
        border-left: 15px solid #ffff00;
        padding-left: 20px;
    }
    
    /* Esconder menus do Streamlit para parecer um software */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO IMPACTANTE
st.markdown('<div class="main-title">FORECAST DE CONSUMO PARA FEVEREIRO</div>', unsafe_allow_html=True)

# 3. DADOS EXATOS DO CONSUMO
dados = {
    'EM': ['CUMARU', 'IPE', 'JATOBA', 'AROEIRA', 'SAMAUAMA', 'ANGICO', 'LUIZ FELIPE', 'JACARANDA', 'CAJERANA', 'QUARUBA'],
    'LITROS': [81628.8, 45777.6, 37804.8, 37804.8, 35706.0, 33079.2, 28934.4, 19588.8, 19588.8, 8395.2],
    'REAIS': [485115.84, 241005.60, 198002.64, 198002.64, 186028.26, 191859.36, 167819.52, 115643.88, 115699.85, 60445.44]
}
df_em = pd.DataFrame(dados)

ciclos = {
    'CICLO': ['CICLO 1', 'CICLO 2', 'CICLO 3', 'CICLO 4'],
    'VOL': [140950, 132488, 13992, 60878],
    'FIN': [818763.26, 724684.62, 86540.52, 329634.62]
}
df_c = pd.DataFrame(ciclos)

# --- GRÁFICO 1: CONSUMO POR EMPURRADOR (BARRAS CIANO + LINHA AMARELA) ---
st.markdown('<div class="sub-title">Consumo por Empurrador (Lts vs R$)</div>', unsafe_allow_html=True)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=df_em['EM'], y=df_em['LITROS'], name='LITROS',
    marker_color='#00f2ff', text=df_em['LITROS'], textposition='outside'
))
fig1.add_trace(go.Scatter(
    x=df_em['EM'], y=df_em['REAIS'], name='CUSTO R$',
    line=dict(color='#ffff00', width=12), mode='lines+markers',
    marker=dict(size=18, symbol='diamond', color='#ffff00')
))

fig1.update_layout(
    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    height=700, font=dict(size=18, color="white"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig1, use_container_width=True)

# --- GRÁFICOS INFERIORES: CICLO DE FEVEREIRO ---
st.markdown('<div class="sub-title">Previsto Ciclo de Fevereiro</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Pizza de Volume Neon
    fig2 = px.pie(df_c, values='VOL', names='CICLO', hole=0.6)
    fig2.update_traces(textinfo='percent+label', marker=dict(colors=['#00f2ff', '#0074d9', '#2ecc40', '#ff4136']))
    fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=22), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    # Tendência Contábil Área Glow
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_c['CICLO'], y=df_c['FIN'], fill='tozeroy',
        line=dict(color='#00ff88', width=10), mode='lines+markers'
    ))
    fig3.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=22), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#30363d')
    )
    st.plotly_chart(fig3, use_container_width=True)
