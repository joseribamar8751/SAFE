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
# CSS PERSONALIZADO (Estilo Dark / Industrial)
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
    
    .status-card-alert {
        background-color: #2a1215;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 12px;
        color: #ef4444;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO (Para manter os valores entre as páginas)
# ==============================================================================
if "temp_simulada" not in st.session_state:
    st.session_state["temp_simulada"] = 48.1

if "vibracao_simulada" not in st.session_state:
    st.session_state["vibracao_simulada"] = 2.4

if "rele_estado" not in st.session_state:
    st.session_state["rele_estado"] = True


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
        index=0,  # Abre por padrão na Planta Industrial
        label_visibility="collapsed"
    )

    st.divider()

    # Exibição do Status Dinâmico baseado nos limites de alarme
    if st.session_state["temp_simulada"] > 70 or st.session_state["vibracao_simulada"] > 4.5 or not st.session_state["rele_estado"]:
        st.markdown("""
            <div class="status-card-alert">
                <strong>⚠️ Ativo em Estado Crítico / Alerta</strong><br>
                <span style="font-size: 0.8em;">Modo de Simulação Ativo</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="status-card-ok">
                <strong>🟢 Todos os ativos normais</strong><br>
                <span style="font-size: 0.8em; color: #9ca3af;">MQTT • 3 gateways ESP32 online</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.caption("Powered by **Gestão da Manutenção**")


# ==============================================================================
# 2.
