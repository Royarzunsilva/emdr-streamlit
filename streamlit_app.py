from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Visor EMDR", page_icon="💧", layout="wide")
st.title("Visor EMDR – Control")

# ── Controles ───────────────────────────────────────────────────
c1, c2 = st.columns(2)
minutes = c1.slider("Duración (min)", 1, 20, 10)
cycle   = c2.slider("Ciclo ida-vuelta (s)", 0.3, 2.0, 0.8, 0.1)

if st.button("Abrir visor"):
    st.success(
        "Se ha abierto una ventana nueva. "
        "Colócala en la pantalla deseada y pulsa F11 para modo completo."
    )

# ── Audio de fondo opcional ─────────────────────────────────────
audio = Path(__file__).parent / "assets" / "relaxing_sound.mp3"
if audio.exists():
    st.audio(str(audio), loop=True)

# ── Genera el código del visor (HTML + CSS + JS) ────────────────
html_popup = f"""
<script>
function openEMDR() {{
  // Calcula tamaño de la pantalla
  const w = screen.width  * 0.95;
  const h = screen.height * 0.95;

  // Crea la nueva ventana
  const win = window.open(
    "", "EMDR_Visor",
    "toolbar=no,menubar=no,location=no," +
    "resizable=yes,scrollbars=no,status=no," +
    `width=${{w}},height=${{h}}`
  );

  if (!win) {{
    alert("El navegador ha bloqueado la ventana emergente. Permite pop-ups.");
    return;
  }}

  // Contenido de la ventana
  win.document.body.style.margin = "0";
  win.document.title = "Visor EMDR";

  win.document.body.innerHTML = `
    <style>
      body  {{background:#0a0a1e;overflow:hidden}}
      #bar  {{
        position:absolute;top:0;left:0;width:12px;height:100%;
        background:#64c8ff;transition:left 30ms linear;
        box-shadow:0 0 12px #64c8ff;
      }}
    </style>
    <div id='bar'></div>
  `;

  const bar  = win.document.getElementById('bar');
  const width= win.innerWidth - 12;
  let pos=0, dir=1,
      px = width / ({cycle}*20); // avance por frame

  function step(){{
    pos += dir*px;
    if(pos<=0||pos>=width) dir*=-1;
    bar.style.left = pos + 'px';
  }}
  const t = setInterval(step,50);
  setTimeout(()=>clearInterval(t), {minutes*60*1000});
}}
openEMDR();
</script>
"""

# ── Inyectar el script si se pulsó el botón ─────────────────────
# (utiliza una clave en el estado para lanzar una sola vez)
if "run_js" not in st.session_state:
    st.session_state.run_js = False

if st.session_state.run_js:
    components.html(html_popup, height=0, width=0)
    st.session_state.run_js = False  # resetea

def click_js():
    st.session_state.run_js = True

# Conectar el callback al botón (Streamlit 1.18+)
st.button("Abrir visor (popup)", key="open_btn", on_click=click_js)
