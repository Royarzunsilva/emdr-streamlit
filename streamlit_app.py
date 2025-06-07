from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ───────────── Configuración de página ─────────────
st.set_page_config(page_title="Visor EMDR", page_icon="💧", layout="wide")

# ───────────── Controles en barra lateral ──────────
with st.sidebar:
    st.title("Visor EMDR – Controles")
    minutes = st.slider("Duración (min)", 1, 20, 10, key="dur")
    cycle   = st.slider("Ciclo ida-vuelta (s)", 0.3, 2.0, 0.8, 0.1, key="cyc")
    audio_on = st.checkbox("Música de fondo", True, key="au")
    start = st.button("Start / Stop", key="btn")

# ───────────── Audio opcional ───────────────────────
audio_path = Path(__file__).parent / "assets" / "relaxing_sound.mp3"
if audio_on and audio_path.exists():
    st.audio(str(audio_path), loop=True)

# ───────────── Control de estado ────────────────────
if start:
    st.session_state.running = not st.session_state.get("running", False)

running = st.session_state.get("running", False)
total_sec = int(st.session_state.get("dur", 10) * 60)
cycle_sec = float(st.session_state.get("cyc", 0.8))

# ───────────── HTML + CSS + JS ──────────────────────
html = f"""
<style>
  html, body {{ margin:0; background:#0a0a1e; }}
  #wrap {{
    position:fixed; top:0; left:0; width:100vw; height:100vh;
    background:#0a0a1e; overflow:hidden;
    display:{'block' if running else 'none'};
  }}
  #bar  {{
    position:absolute; top:0; left:0; width:12px; height:100%;
    background:#64c8ff; box-shadow:0 0 16px #64c8ff;
  }}
  #timer{{
    position:fixed; top:12px; right:18px; padding:4px 12px;
    background:#222e3acc; color:#e0e0e0; font-family:Arial;
    font-size:22px; border-radius:6px;
    display:{'block' if running else 'none'};
  }}
</style>

<div id="wrap"><div id="bar"></div></div>
<div id="timer"></div>

<script>
(function(){{
  const running = {str(running).lower()};
  if(!running) return;

  const dur  = {total_sec};
  const cyc  = {cycle_sec};
  const wrap = document.getElementById('wrap');
  const bar  = document.getElementById('bar');
  const tim  = document.getElementById('timer');

  // Pantalla completa al arrancar
  if (wrap.requestFullscreen) wrap.requestFullscreen();
  else if (wrap.webkitRequestFullscreen) wrap.webkitRequestFullscreen();

  let pos=0, dir=1;
  const width = () => window.innerWidth - 12;
  let px = width() / (cyc*20);
  let remain = dur;

  function step(){{
    pos += dir*px;
    if(pos<=0||pos>=width()) dir*=-1;
    bar.style.left = pos + 'px';
  }}

  function two(n){{return n<10?'0'+n:n;}}
  function tick(){{
    remain--;
    tim.textContent = two(Math.floor(remain/60))+':'+two(remain%60);
    if(remain<=0) stop();
  }}

  function stop(){{
    clearInterval(move); clearInterval(clock);
    if(document.fullscreenElement) document.exitFullscreen();
    setTimeout(()=>location.reload(), 300);  // recarga y muestra controles
  }}

  tim.textContent = two(Math.floor(remain/60))+':'+two(remain%60);
  const move  = setInterval(step, 50);   // ~20 FPS
  const clock = setInterval(tick, 1000);
}})();
</script>
"""

components.html(html, height=0, width=0, scrolling=False)
