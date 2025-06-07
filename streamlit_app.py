from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ───────────── Configuración de página ─────────────
st.set_page_config(page_title="Visor EMDR", page_icon="💧", layout="wide")

# ───────────── Controles en la propia página ───────
with st.sidebar:
    st.title("Visor EMDR – Controles")
    minutes = st.slider("Duración (min)", 1, 20, 10, key="dur")
    cycle   = st.slider("Ciclo ida-vuelta (s)", 0.3, 2.0, 0.8, 0.1, key="cyc")
    audio_on = st.checkbox("Música relajante", True, key="au")
    start = st.button("Start / Stop", key="btn")

# ───────────── Reproduce audio opcional ─────────────
audio_path = Path(__file__).parent / "assets" / "relaxing_sound.mp3"
if audio_on and audio_path.exists():
    st.audio(str(audio_path), loop=True)

# ───────────── Lógica de sesión ─────────────────────
if start:
    st.session_state.run = not st.session_state.get("run", False)

run = st.session_state.get("run", False)
total_sec = int(st.session_state.get("dur", 10) * 60)
cycle_sec = float(st.session_state.get("cyc", 0.8))

html = f"""
<style>
  html, body {{ margin:0; background:#0a0a1e; }}
  #wrap {{ position:fixed; top:0; left:0; width:100vw; height:100vh;
           background:#0a0a1e; overflow:hidden; }}
  #bar  {{ position:absolute; top:0; left:0; width:12px; height:100%;
           background:#64c8ff; box-shadow:0 0 16px #64c8ff; }}
  #timer{{ position:fixed; top:12px; right:18px; padding:4px 12px;
           background:#222e3acc; color:#e0e0e0; font-family:Arial;
           font-size:22px; border-radius:6px; }}
  #overlayControls{{position:fixed; top:0; left:0; width:100%;
           height:100%; display:flex; align-items:center;
           justify-content:center; background:#000a; }}
</style>

<div id="wrap"{' style="display:none;"' if not run else ''}>
  <div id="bar"></div>
  <div id="timer"></div>
</div>

<script>
let running = {str(run).lower()};
const dur  = {total_sec};
const cyc  = {cycle_sec};

function two(n){{return n<10?"0"+n:n}}
function startEMDR(){{
  const wrap=document.getElementById('wrap');
  const bar =document.getElementById('bar');
  const tim =document.getElementById('timer');
  if(!wrap) return;

  // pantalla completa
  if (running){{
    if (wrap.requestFullscreen) wrap.requestFullscreen();
    else if (wrap.webkitRequestFullscreen) wrap.webkitRequestFullscreen();
  }}

  const width = () => window.innerWidth - 12;
  let pos=0, dir=1, px = width() / (cyc*20);
  let leftInt, timeInt, remain=dur;

  function step(){{
    pos += dir*px;
    if(pos<=0||pos>=width()){{dir*=-1}}
    bar.style.left = pos + "px";
  }}
  function tick(){{
    remain--;
    tim.textContent = two(Math.floor(remain/60))+":"+two(remain%60);
    if(remain<=0) stopEMDR();
  }}

  function stopEMDR(){{
    clearInterval(leftInt); clearInterval(timeInt);
    tim.textContent="Fin";
    if(document.fullscreenElement) document.exitFullscreen();
    // pedir al backend que quite running:
    fetch(window.location.href,{{method:"POST"}}).catch(()=>{{}});
  }}

  if(running){{
    tim.textContent = two(Math.floor(remain/60))+":"+two(remain%60);
    leftInt=setInterval(step,50);
    timeInt=setInterval(tick,1000);
  }}
}}
startEMDR();
</script>
"""

# Renderiza el HTML/JS (altura 0 para ocupar toda la ventana)
components.html(html, height=0, width=0, scrolling=False)

# Reset del estado cuando el frontend envía POST (al terminar)
if st.request_method == "POST":
    st.session_state.run = False
