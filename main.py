import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import quote

# Configuração e Estilo Visual (AZUL ESCURO + FONTE 45PX)
st.set_page_config(page_title="CONTROLE DE COMBUSTÍVEL PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #001f3f !important; } /* Fundo Azul Escuro */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 { 
        color: #FFFFFF !important; 
        font-size: 45px !important; 
        font-weight: bold;
        font-family: 'Arial Black', sans-serif;
    }
    /* Estilo dos Cards de Dados */
    div[data-testid="stMetric"] {
        background-color: #003366;
        border: 2px solid #0074D9;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# URL da Planilha
SHEET_ID = '14cRIHelvGZDUcQGcaH2ieBVvl5t36rCPfU2ulmPto8c'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote("Programação")}'

def fix_val(v):
    if pd.isna(v): return 0
    s = str(v).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try: return float(s)
    except: return 0

@st.cache_data(ttl=30)
def get_data():
    df = pd.read_csv(url, header=None)
    # Tabela Unidades (Colunas A, B, C)
    emp = df.iloc[2:12, [0, 1, 2]].copy()
    emp.columns = ['EM', 'LITS', 'REAIS']
    # Tabela Ciclo (Pega as linhas 15 a 18 das colunas A, B, C ou similares)
    cic = df.iloc[14:18, [0, 1, 2]].copy()
    cic.columns = ['CICLO', 'LITS', 'REAIS']
    
    for d in [emp, cic]:
        d.iloc[:, 1] = d.iloc[:, 1].apply(fix_val)
        d.iloc[:, 2] = d.iloc[:, 2].apply(fix_val)
    return emp, cic

try:
    df_emp, df_cic = get_data()

    # --- TÍTULO 1 ---
    st.write("⚓ CONSUMO POR EMPURRADOR")

    # GRÁFICO MISTO: BARRAS (LITROS) + LINHA (CONTÁBIL)
    fig1 = go.Figure()
    # Barras Coloridas (Litros)
    fig1.add_trace(go.Bar(
        x=df_emp['EM'], y=df_emp['LITS'], name='Litros',
        marker_color='cyan', text=df_emp['LITS'], textposition='outside'
    ))
    # Linha Amarela (Custo Contábil)
    fig1.add_trace(go.Scatter(
        x=df_emp['EM'], y=df_emp['REAIS'], name='Custo R$',
        line=dict(color='yellow', width=8), mode='lines+markers+text'
    ))
    
    fig1.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=800, font=dict(size=18), showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- TÍTULO 2 ---
    st.write("📅 PREVISTO CICLO FEVEREIRO")

    c_left, c_right = st.columns(2)

    with c_left:
        # PIZZA PARA VOLUME (LITROS)
        st.write("🍕 VOLUME POR CICLO")
        fig_p = px.pie(df_cic, values='LITS', names='CICLO', color_discrete_sequence=px.colors.qualitative.Set1)
        fig_p.update_traces(textinfo='percent+label', textfont_size=25)
        fig_p.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

    with c_right:
        # LINHA PARA CONTÁBIL (R$)
        st.write("📈 TENDÊNCIA CONTÁBIL")
        fig_l = px.line(df_cic, x='CICLO', y='REAIS', markers=True)
        fig_l.update_traces(line=dict(color='#00FF00', width=10), marker=dict(size=20))
        fig_l.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_l, use_container_width=True)

except Exception as e:
    st.error("ERRO NOS DADOS!")
    st.write(e)
