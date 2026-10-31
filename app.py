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
# 2. ÁREA PRINCIPAL: PLANTA INDUSTRIAL (SIMULADOR DO MOTOR)
# ==============================================================================
if opcao_menu == "🏢 Planta Industrial":
    st.title("🏢 Planta Industrial - Simulador do Motor")
    st.caption("Ajuste as variáveis abaixo para testar a lógica do sistema sem o protótipo físico.")
    st.write("")

    col_sim, col_preview = st.columns([1, 1])

    with col_sim:
        st.subheader("🎛️ Painel de Testes do Motor 01")
        
        # Slider de Temperatura do Motor
        temp = st.slider(
            "🌡️ Temperatura do Motor (°C)", 
            min_value=0.0, 
            max_value=120.0, 
            value=st.session_state["temp_simulada"], 
            step=0.5
        )
        st.session_state["temp_simulada"] = temp

        # Slider de Vibração
        vibr = st.slider(
            "📳 Nível de Vibração (RMS mm/s)", 
            min_value=0.0, 
            max_value=10.0, 
            value=st.session_state["vibracao_simulada"], 
            step=0.1
        )
        st.session_state["vibracao_simulada"] = vibr

        # Toggle/Chave do Relé
        rele = st.toggle("⚡ Módulo Relé (Alimentação do Motor)", value=st.session_state["rele_estado"])
        st.session_state["rele_estado"] = rele

    with col_preview:
        st.subheader("📊 Leitura em Tempo Real (Simulada)")
        
        # Card com o Status Atual do Motor
        status_texto = "NORMAL" if (temp <= 70 and vibr <= 4.5 and rele) else "ALERTA"
        cor_status = "#00e676" if status_texto == "NORMAL" else "#ef4444"
        
        st.markdown(f"""
            <div class="metric-card">
                <h4>Motor Trifásico - Exaustor 02</h4>
                <p>Status: <b style="color:{cor_status};">{status_texto}</b></p>
                <hr style="border-color: #1e2d42;">
                <p><b>Temperatura do Motor:</b> {temp} °C</p>
                <p><b>Vibração do Motor:</b> {vibr} mm/s</p>
                <p><b>Relé de Potência:</b> {"🟢 LIGADO" if rele else "🔴 DESLIGADO"}</p>
            </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 3. ÁREA PRINCIPAL: DIAGNÓSTICO DO ATIVO (CONECTADO AO SIMULADOR)
# ==============================================================================
elif opcao_menu == "📈 Diagnóstico do Ativo":
    st.title("Diagnóstico do Ativo")
    st.caption("Setor de Ventilação • Exaustor 02 • Módulo MCSA + FFT (Edge AI)")
    st.write("")

    # Calcula a saúde estimada com base nos valores simulados
    temp_val = st.session_state["temp_simulada"]
    vibr_val = st.session_state["vibracao_simulada"]
    rele_val = st.session_state["rele_estado"]

    # Lógica simples de cálculo de saúde
    saude_pct = 100
    if temp_val > 50:
        saude_pct -= (temp_val - 50) * 1.2
    if vibr_val > 2.5:
        saude_pct -= (vibr_val - 2.5) * 8
    if not rele_val:
        saude_pct = 0

    saude_pct = max(0, min(100, int(saude_pct))) # Garante entre 0% e 100%
    cor_saude = "#00e676" if saude_pct > 70 else ("#f59e0b" if saude_pct > 40 else "#ef4444")

    # --- CARD PRINCIPAL: ÍNDICE DE SAÚDE SAFE ---
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #94a3b8;'>ÍNDICE DE SAÚDE SAFE</h4>", unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Pie(
            values=[saude_pct, 100 - saude_pct],
            hole=0.75,
            marker_colors=[cor_saude, '#112233'],
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
                'text': f"<b>{saude_pct}%</b><br><span style='font-size:14px;color:{cor_saude};'>{'SAUDÁVEL' if saude_pct > 70 else 'ATENÇÃO'}</span>",
                'x': 0.5, 'y': 0.5,
                'font_size': 36,
                'font_color': "#ffffff",
                'showarrow': False
            }]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- CARTÕES INFERIORES: SENSORES ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8; font-size: 14px;">Temperatura do Motor</span>
                    <span style="font-size: 20px;">🌡️</span>
                </div>
                <h1 style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold;">{temp_val:.1f} <span style="font-size: 20px;">°C</span></h1>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8; font-size: 14px;">Vibração do Motor</span>
                    <span style="font-size: 20px;">📳</span>
                </div>
                <h1 style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold;">{vibr_val:.1f} <span style="font-size: 20px;">mm/s</span></h1>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8; font-size: 14px;">Módulo Relé</span>
                    <span style="font-size: 20px;">⚡</span>
                </div>
                <h1 style="margin: 10px 0 0 0; font-size: 30px; font-weight: bold; color: {'#00e676' if rele_val else '#ef4444'};">
                    {'LIGADO' if rele_val else 'DESLIGADO'}
                </h1>
            </div>
        """, unsafe_allow_html=True)

else:
    st.title(opcao_menu)
    st.info("Página em desenvolvimento. NAVEGUE ATRAVÉS DA BARRA LATERAL.")
