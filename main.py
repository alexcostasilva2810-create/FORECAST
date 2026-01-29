import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. DESIGN E CONFIGURAÇÃO
st.set_page_config(page_title="BI OPERACIONAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030a1c !important; }
    .main-title { font-size: 55px !important; color: #00f2ff !important; text-align: center; font-weight: 900; padding: 20px; border-bottom: 3px solid #00f2ff; }
    .sub-title { font-size: 35px !important; color: #ffffff !important; font-weight: 700; border-left: 10px solid #ffff00; padding-left: 15px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS (ESTRUTURADOS PARA FILTRAGEM)
@st.cache_data
def get_data():
    unidades = ['CUMARU', 'IPE', 'JATOBA', 'AROEIRA', 'SAMAUAMA', 'ANGICO', 'LUIZ FELIPE', 'JACARANDA', 'CAJERANA', 'QUARUBA']
    litros = [81628.8, 45777.6, 37804.8, 37804.8, 35706.0, 33079.2, 28934.4, 19588.8, 19588.8, 8395.2]
    reais = [485115.84, 241005.60, 198002.64, 198002.64, 186028.26, 191859.36, 167819.52, 115643.88, 115699.85, 60445.44]
    
    # Criando DataFrame completo
    df = pd.DataFrame({'EM': unidades, 'LITROS': litros, 'REAIS': reais})
    
    # Dados de Ciclo (Exemplo relacionado)
    ciclos = pd.DataFrame({
        'EM': unidades * 4,
        'CICLO': (['CICLO 1']*10 + ['CICLO 2']*10 + ['CICLO 3']*10 + ['CICLO 4']*10),
        'VOL': [l/4 for l in litros*4],
        'FIN': [r/4 for r in reais*4]
    })
    return df, ciclos

df_main, df_ciclos_full = get_data()

# 3. LÓGICA DE FILTRAGEM (O SEGREDO DO POWER BI NO STREAMLIT)
if 'filtro_unidade' not in st.session_state:
    st.session_state.filtro_unidade = None

def filtrar_unidade():
    if st.session_state.unidade_selecionada:
        st.session_state.filtro_unidade = st.session_state.unidade_selecionada

# TÍTULO
st.markdown('<div class="main-title">DASHBOARD INTERATIVO - FORECAST FEVEREIRO</div>', unsafe_allow_html=True)

# BARRA LATERAL PARA FILTRO (COMO O FILTRO DE SLICER DO BI)
with st.sidebar:
    st.markdown("### 🔍 FILTROS")
    unidade_selecionada = st.selectbox("Selecione o Empurrador:", [None] + list(df_main['EM'].unique()))
    if st.button("LIMPAR FILTROS"):
        st.session_state.filtro_unidade = None
        st.rerun()

# APLICANDO O FILTRO AOS DADOS
df_filtrado = df_main.copy()
df_ciclos_filtrado = df_ciclos_full.copy()

if unidade_selecionada:
    df_filtrado = df_main[df_main['EM'] == unidade_selecionada]
    df_ciclos_filtrado = df_ciclos_full[df_ciclos_full['EM'] == unidade_selecionada]

# --- LAYOUT DOS GRÁFICOS ---
st.markdown(f'<div class="sub-title">Análise: {unidade_selecionada if unidade_selecionada else "TODOS"}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico Misto que responde ao clique/seleção
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df_filtrado['EM'], y=df_filtrado['LITROS'], name='LITROS', marker_color='#00f2ff'))
    fig1.add_trace(go.Scatter(x=df_filtrado['EM'], y=df_filtrado['REAIS'], name='CONTÁBIL', line=dict(color='#ffff00', width=6)))
    
    fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    # Agrupamento por Ciclo baseado no filtro
    df_c_resumo = df_ciclos_filtrado.groupby('CICLO').sum().reset_index()
    fig2 = px.pie(df_c_resumo, values='VOL', names='CICLO', hole=0.5, title="DISTRIBUIÇÃO POR CICLO")
    fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    fig3 = px.line(df_c_resumo, x='CICLO', y='FIN', title="TENDÊNCIA FINANCEIRA DO FILTRO", markers=True)
    fig3.update_traces(line_color='#00ff88', width=8)
    fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)
