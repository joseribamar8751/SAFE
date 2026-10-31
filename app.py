import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página em modo WIDE
st.set_page_config(
    page_title="SAFE - Diagnóstico do Ativo", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS PERSONALIZADO (Para replicar as cores escurecidas e estilo do layout)
# ==============================================================================
st.markdown("""
    <style>
    /* Fundo principal da aplicação */
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    
    /* Fundo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #080b11;
        border-right: 1px solid #1e293b;
    }
    
    /* Estilo dos cartões (Cards) */
    .metric-card {
        background-color: #111726;
        border: 1px solid #1e2d42;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .status-card-ok {
        background-color: #0d211a;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 12px;
        color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. BARRA LATERAL (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown("## 🛡️ **SAFE**")
    st.caption("Sistema de Alerta e Fiscalização de Equipamentos")
    st.divider()

    # Menu de Navegação
    opcao_menu = st.radio(
        "Navegação",
        [
            "🏢 Planta Industrial", 
            "📈 Diagnóstico do Ativo", 
            "📋 Ordens de Serviço", 
            "📦 Almoxarifado & Compras", 
            "📊 KPIs & Gestão à Vista"
        ],
        index=1,
        label_visibility="collapsed"
    )

    st.divider()

    # Box de Status (Conectividade MQTT / ESP32)
    st.markdown("""
        <div class="status-card-ok">
            <strong>🟢 Todos os ativos normais</strong><br>
            <span style="font-size: 0.8em; color: #9ca3af;">MQTT • 3 gateways ESP32 online</span>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.caption("Powered by **Gestão da Manutenção**")


# ==============================================================================
# 2. ÁREA PRINCIPAL - DIAGNÓSTICO DO ATIVO
# ==============================================================================
if "Diagnóstico do Ativo" in opcao_menu:
    
    # Cabeçalho da Página
    st.title("Diagnóstico do Ativo")
    st.caption("Setor de Ventilação • Exaustor 02 • Módulo MCSA + FFT (Edge AI)")
    st.write("")

    # --- CARD PRINCIPAL: ÍNDICE DE SAÚDE SAFE ---
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #94a3b8;'>ÍNDICE DE SAÚDE SAFE</h4>", unsafe_allow_html=True)
        
        # Gráfico de Rosca (Donut Chart) estilo "Gauge"
        saude_pct = 95
        
        fig = go.Figure(data=[go.Pie(
            values=[saude_pct, 100 - saude_pct],
            hole=0.75,
            marker_colors=['#00e676', '#112233'],
            textinfo='none',
            hoverinfo='none'
        )])

        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=220,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[{
                'text': f"<b>{saude_pct}%</b><br><span style='font-size:14px;color:#00e676;'>SAUDÁVEL</span>",
                'x': 0.5, 'y': 0.5,
                'font_size': 36,
                'font_color': "#ffffff",
                'showarrow': False
            }]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<p style='text-align: center; color: #94a3b8;'>Próxima intervenção estimada: <b>142 dias</b></p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- CARTÕES INFERIORES: SENSORES E MEDIÇÕES ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94a3b8; font-size: 14px;">Temperatura do Mancal</span>
                    <span style="color: #00e676; font-size: 20px;">🌡️</span>
                </div>
                <h1 style="margin: 10px 0 0 0; font-size: 40px; font-weight: bold;">48.1 <span style="font-size: 24px;">°C</span></h1>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94a3b8; font-size: 14px;">Corrente (RMS)</span>
                    <span style="color: #00e676; font-size: 20px;">🔄</span>
                </div>
                <h1 style="margin: 5px 0 0 0; font-size: 40px; font-weight: bold;">7.62 <span style="font-size: 24px;">A</span></h1>
                <span style="color: #64748b; font-size: 12px;">Nominal 7,6 A</span>
            </div>
        """, unsafe_allow_html=True)

else:
    st.title(opcao_menu)
    st.info("Selecione 'Diagnóstico do Ativo' na barra lateral para visualizar a tela configurada.")    
