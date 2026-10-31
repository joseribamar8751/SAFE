import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# Configuração da página em modo WIDE
st.set_page_config(
    page_title="SAFE - Diagnóstico do Ativo",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# CSS PERSONALIZADO (Estilo Dark / Industrial)
# ==============================================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0f19; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #080b11; border-right: 1px solid #1e293b; }
    .metric-card { background-color: #111726; border: 1px solid #1e2d42; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .status-card-ok { background-color: #0d211a; border: 1px solid #10b981; border-radius: 10px; padding: 12px; color: #10b981; }
    .status-card-alert { background-color: #2a1215; border: 1px solid #ef4444; border-radius: 10px; padding: 12px; color: #ef4444; }
    </style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# FUNÇÃO PARA ENVIAR ALERTA VIA WHATSAPP CLOUD API (META)
# ==============================================================================
def enviar_alerta_whatsapp_meta(
    phone_number_id, bearer_token, numero_destino
):
  url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"

  headers = {
      "Authorization": f"Bearer {bearer_token}",
      "Content-Type": "application/json",
  }

  payload = {
      "messaging_product": "whatsapp",
      "to": numero_destino,
      "type": "template",
      "template": {"name": "hello_world", "language": {"code": "en_US"}},
  }

  try:
    resposta = requests.post(url, headers=headers, json=payload, timeout=5)
    dados = resposta.json()
    if "messages" in dados:
      return True, "Mensagem enviada com sucesso!"
    else:
      erro_msg = dados.get("error", {}).get("message", "Erro desconhecido")
      return False, erro_msg
  except Exception as e:
    return False, str(e)


# ==============================================================================
# INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO
# ==============================================================================
if "temp_simulada" not in st.session_state:
  st.session_state["temp_simulada"] = 48.1

if "vibracao_simulada" not in st.session_state:
  st.session_state["vibracao_simulada"] = 2.4

if "rele_estado" not in st.session_state:
  st.session_state["rele_estado"] = True

if "alerta_enviado" not in st.session_state:
  st.session_state["alerta_enviado"] = False


# ==============================================================================
# 1. BARRA LATERAL (SIDEBAR)
# ==============================================================================
with st.sidebar:
  st.markdown("## 🛡️ **SAFE**")
  st.caption("Sistema de Alerta e Fiscalização de Equipamentos")
  st.divider()

  opcao_menu = st.radio(
      "Navegação",
      [
          "🏢 Planta Industrial",
          "📈 Diagnóstico do Ativo",
          "📋 Ordens de Serviço",
          "📦 Almoxarifado & Compras",
          "📊 KPIs & Gestão à Vista",
      ],
      index=0,
      label_visibility="collapsed",
  )

  st.divider()

  if (
      st.session_state["temp_simulada"] > 70
      or st.session_state["vibracao_simulada"] > 4.5
      or not st.session_state["rele_estado"]
  ):
    st.markdown(
        """
            <div class="status-card-alert">
                <strong>⚠️ Ativo em Estado Crítico / Alerta</strong><br>
                <span style="font-size: 0.8em;">Modo de Simulação Ativo</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """
            <div class="status-card-ok">
                <strong>🟢 Todos os ativos normais</strong><br>
                <span style="font-size: 0.8em; color: #9ca3af;">MQTT • 3 gateways ESP32 online</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.caption("Powered by **Gestão da Manutenção**")


# ==============================================================================
# 2. ÁREA PRINCIPAL: PLANTA INDUSTRIAL (SIMULADOR DO MOTOR + WHATSAPP CLOUD)
# ==============================================================================
if opcao_menu == "🏢 Planta Industrial":
  st.title("🏢 Planta Industrial - Simulador do Motor")
  st.caption(
      "Ajuste as variáveis e os limites para disparar notificações oficiais no"
      " WhatsApp."
  )
  st.write("")

  col_sim, col_wa = st.columns([1, 1])

  with col_sim:
    st.subheader("🎛️ Painel de Testes do Motor 01")

    temp = st.slider(
        "🌡️ Temperatura do Motor (°C)",
        min_value=0.0,
        max_value=120.0,
        value=st.session_state["temp_simulada"],
        step=0.5,
    )
    st.session_state["temp_simulada"] = temp

    vibr = st.slider(
        "📳 Nível de Vibração (RMS mm/s)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state["vibracao_simulada"],
        step=0.1,
    )
    st.session_state["vibracao_simulada"] = vibr

    rele = st.toggle(
        "⚡ Módulo Relé (Alimentação do Motor)",
        value=st.session_state["rele_estado"],
    )
    st.session_state["rele_estado"] = rele

  with col_wa:
    st.subheader("🟢 WhatsApp Cloud API (Meta)")

    limite_temp = st.number_input(
        "Limite Máximo de Temperatura (°C):", value=70.0, step=1.0
    )
    limite_vibr = st.number_input(
        "Limite Máximo de Vibração (mm/s):", value=4.5, step=0.5
    )

    st.divider()
    st.caption("Insira as credenciais do seu aplicativo Meta Developer:")

    meta_phone_id = st.text_input(
        "Phone Number ID:", placeholder="Cole o ID numérico do seu número"
    )
    meta_token = st.text_input(
        "Temporary Access Token:",
        type="password",
        placeholder="Cole o token copiado",
    )
    num_celular = st.text_input(
        "Seu Celular (Com DDD, sem o +):", placeholder="Ex: 5511999998888"
    )

  # --- LÓGICA DE DISPARO DE ALERTA ---
  critico_temp = temp > limite_temp
  critico_vibr = vibr > limite_vibr
  critico_rele = not rele

  if critico_temp or critico_vibr or critico_rele:
    motivo = []
    if critico_temp:
      motivo.append(f"Temperatura alta ({temp}°C > {limite_temp}°C)")
    if critico_vibr:
      motivo.append(f"Vibração alta ({vibr} mm/s > {limite_vibr} mm/s)")
    if critico_rele:
      motivo.append("Relé DESLIGADO")

    st.error(f"🚨 **ALERTA DETECTADO!** Motivos: {', '.join(motivo)}")

    if (
        meta_phone_id
        and meta_token
        and num_celular
        and not st.session_state["alerta_enviado"]
    ):
      sucesso, log = enviar_alerta_whatsapp_meta(
          meta_phone_id, meta_token, num_celular
      )

      if sucesso:
        st.success("📲 Notificação enviada para o seu WhatsApp com sucesso!")
        st.session_state["alerta_enviado"] = True
      else:
        st.warning(f"Erro ao enviar WhatsApp: {log}")
  else:
    st.session_state["alerta_enviado"] = False


# ==============================================================================
# 3. ÁREA PRINCIPAL: DIAGNÓSTICO DO ATIVO
# ==============================================================================
elif opcao_menu == "📈 Diagnóstico do Ativo":
  st.title("Diagnóstico do Ativo")
  st.caption("Setor de Ventilação • Exaustor 02 • Módulo MCSA + FFT (Edge AI)")
  st.write("")

  temp_val = st.session_state["temp_simulada"]
  vibr_val = st.session_state["vibracao_simulada"]
  rele_val = st.session_state["rele_estado"]

  saude_pct = 100
  if temp_val > 50:
    saude_pct -= (temp_val - 50) * 1.2
  if vibr_val > 2.5:
    saude_pct -= (vibr_val - 2.5) * 8
  if not rele_val:
    saude_pct = 0

  saude_pct = max(0, min(100, int(saude_pct)))
  cor_saude = (
      "#00e676"
      if saude_pct > 70
      else ("#f59e0b" if saude_pct > 40 else "#ef4444")
  )
  status_texto = "SAUDÁVEL" if saude_pct > 70 else "ATENÇÃO"

  with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align: center; color: #94a3b8;'>ÍNDICE DE SAÚDE"
        " SAFE</h4>",
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        data=[
            go.Pie(
                values=[saude_pct, 100 - saude_pct],
                hole=0.75,
                marker_colors=[cor_saude, "#112233"],
                textinfo="none",
                hoverinfo="none",
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[{
            "text": (
                f"<b>{saude_pct}%</b><br><span"
                f" style='font-size:14px;color:{cor_saude};'>{status_texto}</span>"
            ),
            "x": 0.5,
            "y": 0.5,
            "font_size": 36,
            "font_color": "#ffffff",
            "showarrow": False,
        }],
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns(3)

  with col1:
    st.markdown(
        f"""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 14px;">Temperatura do Motor</span>
                <h1 style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold;">{temp_val:.1f} <span style="font-size: 20px;">°C</span></h1>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    st.markdown(
        f"""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 14px;">Vibração do Motor</span>
                <h1 style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold;">{vibr_val:.1f} <span style="font-size: 20px;">mm/s</span></h1>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
    st.markdown(
        f"""
            <div class="metric-card">
                <span style="color: #94a3b8; font-size: 14px;">Módulo Relé</span>
                <h1 style="margin: 10px 0 0 0; font-size: 30px; font-weight: bold; color: {'#00e676' if rele_val else '#ef4444'};">
                    {'LIGADO' if rele_val else 'DESLIGADO'}
                </h1>
            </div>
        """,
        unsafe_allow_html=True,
    )

else:
  st.title(opcao_menu)
  st.info("Página em desenvolvimento.")
