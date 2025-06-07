from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ─────────── Fondo unificado ────────────
st.markdown(
    """
    <style>
      /* Fondo general de la app */
      .reportview-container, .main, .block-container {
        background-color: #0a0a1e !important;
        color: #e0e0e0;
      }
      /* Barra lateral */
      .sidebar .sidebar-content {
        background-color: #0a0a1e !important;
      }
      /* Elimina márgenes internos de Streamlit */
      .css-12oz5g7, .css-18e3th9 {
        padding: 0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────────── CONFIGURACIÓN ─────────────
st.set_page_config(page_title="Visor EMDR", page_icon="💧", layout="wide")

# ───────────── CONTROLES (SIDEBAR) ───────
with st.sidebar:
    st.title("Visor EMDR – Controles")
    minutes = st.slider("Duración (min)", 1, 20, 10, key="dur")
    cycle   = st.slider("Ciclo ida-vuelta (s)", 0.3, 2.0, 0.8, 0.1, key="cyc")
    audio_on = st.checkbox("Música relajante", True, key="aud")
    if st.button("Start / Stop"):
        st.session_state.running = not st.session_state.get("running", False)

running   = st.session_state.get("running", False)
total_sec = int(minutes * 60)
cycle_sec = float(cycle)

# ───────────── AUDIO (OPCIONAL) ──────────
audio_path = Path(__file__).parent / "assets" / "relaxing_sound.mp3"
if audio_on and audio_path.exists():
    st.audio(str(audio_path), loop=True)

# ───────────── HTML + CSS + JS ───────────
html = f"""
<style>
  html,body {{
    margin:0; padding:0; background:#0a0a1e;
  }}
  #wrap {{
    position:fixed; top:0; left:0;
    width:100vw; height:100vh; background:#0a0a1e;
    overflow:hidden; display:{'block' if running else 'none'};
  }}
  #bar {{
    position:absolute; top:0; left:0; width:12px; height:100%;
    background:#64c8ff; box-shadow:0 0 16px #64c8ff;
  }}
  #timer {{
    position:fixed; top:14px; right:20px;
    padding:4px 14px; background:#222e3acc;
    color:#e0e0e0; font:22px/26px Arial; border-radius:6px;
    display:{'block' if running else 'none'};
  }}
</style>

<div id="wrap"><div id="bar"></div></div>
<div id="timer"></div>

<script>
(function() {{
  const running = {str(running).lower()};
  if (!running) return;

  // Parámetros
  const DUR = {total_sec};          // segundos totales
  const CYC = {cycle_sec};          // un ciclo ida-vuelta
  const BAR = document.getElementById('bar');
  const TIM = document.getElementById('timer');
  const WRAP = document.getElementById('wrap');

  // Solicitar fullscreen
  if (WRAP.requestFullscreen) WRAP.requestFullscreen();
  else if (WRAP.webkitRequestFullscreen) WRAP.webkitRequestFullscreen();

  // Utilidades
  const two = n => n<10 ? '0'+n : n;
  let remain = DUR;
  let pos = 0, dir = 1;
  const width = () => window.innerWidth - 12;
  let px = width() / (CYC * 20);      // avance ≈50 ms (20 FPS)

  // Actualiza cada segundo el temporizador
  function tick() {{
    remain--;
    TIM.textContent = two(Math.floor(remain/60))+':'+two(remain%60);
    if (remain <= 0) stop();
  }}

  // Mueve la barra
  function step() {{
    pos += dir * px;
    if (pos <= 0 || pos >= width()) dir *= -1;
    BAR.style.left = pos + 'px';
  }}

  function stop() {{
    clearInterval(move); clearInterval(clock);
    if (document.fullscreenElement) document.exitFullscreen();
    // Pequeña espera para que salga de fullscreen y recargue
    setTimeout(() => location.reload(), 400);
  }}

  // Primer valor del timer
  TIM.textContent = two(Math.floor(remain/60))+':'+two(remain%60);

  // Inicia intervalos
  const move  = setInterval(step, 50);
  const clock = setInterval(tick, 1000);

  // Si el usuario pulsa Escape (sale de fullscreen), detener también
  document.addEventListener('fullscreenchange', () => {{
    if (!document.fullscreenElement) stop();
  }});
}})();
</script>
"""

# Altura 600 px es suficiente para que el iframe sea visible;
# la barra está en posición fixed, llenará la pantalla completa.
components.html(html, height=600, scrolling=False)
