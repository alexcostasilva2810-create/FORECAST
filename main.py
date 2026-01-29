import streamlit as st
import plotly.graph_objects as go

# Estilo de Fundo e Fonte
st.markdown("""
    <style>
    .main { background-color: #001f3f !important; }
    h1, p, div { color: white !important; font-family: 'Arial Black'; font-size: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

# Dados enviados
dados = {
    'EM': ['CUMARU', 'SAMAUAMA', 'JATOBA', 'LUIZ FELIPE', 'IPE', 'AROEIRA', 'ANGICO', 'JACARANDA', 'CAJERANA', 'QUARUBA'],
    'LITROS': [81628.8, 35706, 37804.8, 28934.4, 45777.6, 37804.8, 33079.2, 19588.8, 19588.8, 8395.2],
    'REAIS': [485115.84, 186028.26, 198002.64, 167819.52, 241005.60, 198002.64, 191859.36, 115643.88, 115699.85, 60445.44]
}

fig = go.Figure()

# Barras de Litros
fig.add_trace(go.Bar(x=dados['EM'], y=dados['LITROS'], name='LITROS', 
                     marker_color='cyan', text=dados['LITROS'], textposition='outside'))

# Linha de Custo Contábil
fig.add_trace(go.Scatter(x=dados['EM'], y=dados['REAIS'], name='R$ CONTÁBIL', 
                         line=dict(color='yellow', width=8), mode='lines+markers'))

fig.update_layout(template="plotly_dark", paper_bgcolor='#001f3f', plot_bgcolor='#001f3f', height=800)
st.plotly_chart(fig, use_container_width=True)
