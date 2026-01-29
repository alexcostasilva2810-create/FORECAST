import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. SETUP DE DESIGN (AZUL-NEGRO + FONTES 45PX)
st.set_page_config(page_title="FORECAST FEVEREIRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030a1c !important; }
    .main-title { font-size: 60px !important; color: #00f2ff !important; text-align: center; font-weight: 900; padding: 30px; border-bottom: 5px solid #00f2ff; }
    .sub-title { font-size: 45px !important; color: #ffffff !important; font-weight: 800; border-left: 15px solid #ffff00; padding-left: 20px; margin-top: 40px; }
    div[data-testid="stSidebar"] { background-color: #050e21 !important; border-right: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DE DADOS (DADOS DE FEVEREIRO)
@st.cache_data
def load_data():
    dados = {
        'EM': ['CUMARU', 'IPE', 'JATOBA', 'AROEIRA', 'SAMAUAMA', 'ANGICO', 'LUIZ FELIPE', 'JACARANDA', 'CAJERANA', 'QUARUBA'],
        'LITROS': [81628.8, 45777.6, 37804.8, 37804.8, 35706.0, 33079.2, 28934.4, 19588.8, 19588.8, 8395.2],
        'REAIS': [485115.84, 241005.60, 198002.64, 198002.64, 186028.26, 191859.36, 167819.52, 115643.88, 115699.85, 60445.44]
    }
    df = pd.DataFrame(dados)
    
    # Dados de Ciclo (Baseados na sua imagem)
    ciclos = pd.DataFrame({
        'EM': ['CUMARU']*4 + ['IPE']*4 + ['JATOBA']*4, # Exemplo de vinculo para filtro
        'CICLO': ['CICLO 1', 'CICLO 2', 'CICLO 3', 'CICLO 4'] * 3,
        'VOL': [140950, 132488, 13992, 60878] * 3,
        'FIN': [818763.26, 724684.62, 86540.52, 329634.62] * 3
    })
    return df, ciclos

df_main, df_ciclos = load_data()

# 3. INTERATIVIDADE (FILTRO SLICER - ESTILO POWER BI)
with st.sidebar:
    st.markdown("### 🔍 FILTROS")
    unidade = st.selectbox("Selecione a Unidade:", [None] + list(df_main['EM'].unique()))
    if st.button("RESTAURAR TUDO"):
        st.rerun()

# APLICANDO FILTROS
df_f = df_main[df_main['EM'] == unidade] if unidade else df_main
df_c_f = df_ciclos[df_ciclos['EM'] == unidade] if unidade else df_ciclos.groupby('CICLO').sum().reset_index()

# TÍTULOS
st.markdown('<div class="main-title">FORECAST DE CONSUMO PARA FEVEREIRO</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Análise: {unidade if unidade else "TOTAL GERAL"}</div>', unsafe_allow_html=True)

# 4. GRÁFICOS INTERATIVOS
col_main = st.columns(1)[0]
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=df_f['EM'], y=df_f['LITROS'], name='LITROS', marker_color='#00f2ff'))
fig1.add_trace(go.Scatter(x=df_f['EM'], y=df_f['REAIS'], name='CUSTO R$', line=dict(color='#ffff00', width=10)))

fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=600, font=dict(size=20))
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    fig2 = px.pie(df_c_f, values='VOL', names='CICLO', hole=0.6, title="DISTRIBUIÇÃO VOLUME")
    fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=22))
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    fig3 = px.line(df_c_f, x='CICLO', y='FIN', title="TENDÊNCIA CONTÁBIL", markers=True)
    fig3.update_traces(line=dict(color='#00ff88', width=12), marker=dict(size=20))
    fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=22))
    st.plotly_chart(fig3, use_container_width=True)
