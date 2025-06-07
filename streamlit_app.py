import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ─────────────────── CONFIGURACIÓN DE PÁGINA ───────────────────
st.set_page_config(
    page_title="Visor EMDR",
    page_icon="💧",
    layout="wide",
)

st.title("Visor EMDR (estimulación bilateral)")

# ────────────────────────── CONTROLES ──────────────────────────
col1, col2 = st.columns(2)
minutes = col1.slider("Duración (min)", 1, 20, 10)
cycle   = col2.slider("Ciclo ida-vuelta (s)", 0.3, 2.0, 0.8, 0.1)
start   = st.button("Iniciar sesión")

# ───────────────────── AUDIO OPCIONAL ──────────────────────────
audio_path = Path(__file__).parent / "assets" / "relaxing_sound.mp3"
if audio_path.exists():
    st.audio(str(audio_path), loop=True)
else:
    st.info("Sube assets/relaxing_sound.mp3 para música ambiente (opcional)")

# ────────────────── FUNCIÓN PRINCIPAL EMDR ─────────────────────
def emdr_session(total_sec: int, cycle_sec: float):
    """Renderiza barra que se desplaza izquierda-derecha durante total_sec."""
    html = f"""
    <style>
      #wrap {{
        position: relative;
        width: 100%;
        height: 120px;
        background: #0a0a1e;
        overflow: hidden;
        border-radius: 4px;
      }}
      #bar {{
        position: absolute;
        top: 10px;
        left: 0;
        width: 8px;
        height: 100px;
        background: #64c8ff;
        transition: left 30ms linear;
      }}
    </style>

    <div id="wrap"><div id="bar"></div></div>

    <script>
      const bar  = document.getElementById('bar');
      const wrap = document.getElementById('wrap');

      let pos = 0;
      let dir = 1;                                   // 1 → derecha, -1 → izquierda
      const px  = (wrap.clientWidth - 8) / ({cycle_sec} * 20);  // avance por frame (~50 ms)

      function step() {{
        pos += dir * px;
        if (pos <= 0 || pos >= wrap.clientWidth - 8) {{
          dir *= -1;
        }}
        bar.style.left = pos + 'px';
      }}

      const timer = setInterval(step, 50);           // ~20 FPS
      setTimeout(() => clearInterval(timer), {total_sec*1000});
    </script>
    """
    # Altura 140 px para que se vea la barra completa
    components.html(html, height=140, scrolling=False)

# ──────────────────── EJECUCIÓN DE SESIÓN ──────────────────────
if start:
    emdr_session(minutes * 60, cycle)
    st.success("Sesión terminada")
