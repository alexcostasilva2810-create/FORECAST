import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. SETUP DE DESIGN (FUNDO AZUL-NEGRO + FONTES NEON)
st.set_page_config(page_title="OPERAÇÃO FEVEREIRO", layout="wide")

st.markdown("""
    <style>
    /* Fundo Escuro Profundo */
    .main { background-color: #050a18 !important; }
    
    /* Fonte 45px em todo o app */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, div { 
        color: #e0e0e0 !important; 
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }

    /* Cabeçalho Especial */
    .header-style {
        font-size: 60px !important;
        color: #00f2ff !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
        padding: 20px;
        border-bottom: 4px solid #00f2ff;
        margin-bottom: 50px;
    }
    
    /* Estilo dos Títulos de Gráfico */
    .graph-title {
        font-size: 45px !important;
        color: #ffffff;
        margin-top: 30px;
        border-left: 10px solid #ffff00;
        padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO
st.markdown('<div class="header-style">Forecast de consumo para Fevereiro</div>', unsafe_allow_html=True)

# 3. BASE DE DADOS (Pé na porta)
dados = {
    'EM': ['CUMARU', 'IPE', 'JATOBA', 'AROEIRA', 'SAMAUAMA', 'ANGICO', 'LUIZ FELIPE', 'JACARANDA', 'CAJERANA', 'QUARUBA'],
    'LITROS': [81628.8, 45777.6, 37804.8, 37804.8, 35706.0, 33079.2, 28934.4, 19588.8, 19588.8, 8395.2],
    'REAIS': [485115.84, 241005.60, 198002.64, 198002.64, 186028.26, 191859.36, 167819.52, 115643.88, 115699.85, 60445.44],
    'CICLO': ['CICLO 1', 'CICLO 2', 'CICLO 3', 'CICLO 4'],
    'VOL_C': [140950, 132488, 13992, 60878],
    'RS_C': [818763.26, 724684.62, 86540.52, 329634.62]
}

# --- GRÁFICO 1: CONSUMO POR EMPURRADOR (COM LINHA DE CUSTO) ---
st.markdown('<div class="graph-title">Consumo por Empurrador (Lts vs R$)</div>', unsafe_allow_html=True)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=dados['EM'], y=dados['LITROS'], name='LITROS',
    marker=dict(color='#00f2ff', line=dict(color='#ffffff', width=1)),
    text=dados['LITROS'], textposition='outside'
))
fig1.add_trace(go.Scatter(
    x=dados['EM'], y=dados['REAIS'], name='CUSTO R$',
    line=dict(color='#ffff00', width=12), mode='lines+markers',
    marker=dict(size=18, symbol='diamond')
))

fig1.update_layout(
    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    height=700, font=dict(size=18), legend=dict(orientation="h", y=1.1)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- GRÁFICOS INFERIORES: CICLO DE FEVEREIRO ---
st.markdown('<div class="graph-title">Previsto Ciclo de Fevereiro</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    # Pizza de Volume
    fig2 = px.pie(values=dados['VOL_C'], names=dados['CICLO'], hole=0.6)
    fig2.update_traces(textinfo='percent+label', marker=dict(colors=['#00f2ff', '#0074d9', '#2ecc40', '#ff4136']))
    fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    # Tendência Contábil
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=dados['CICLO'], y=dados['RS_C'], fill='tozeroy',
        line=dict(color='#00ff88', width=10), mode='lines+markers'
    ))
    fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)
