import streamlit as st, time

st.set_page_config(page_title="Visor EMDR", page_icon="💧", layout="wide")

# ── Controles ─────────────────────────────────
col1, col2 = st.columns(2)
minutes    = col1.slider("Duración (min)", 1, 20, 10)
cycle      = col2.slider("Ciclo ida-vuelta (s)", 0.3, 2.0, 0.8, 0.1)
start_btn  = st.button("Iniciar sesión")

# Audio opcional
try:
    st.audio("assets/relaxing_sound.mp3", loop=True)
except FileNotFoundError:
    pass

# ── Rutina EMDR ───────────────────────────────
def emdr_session(total_sec, cycle_sec):
    block = """
    <style>
      #wrap{position:relative;width:100%;height:120px;background:#0a0a1e}
      #bar{position:absolute;top:10px;width:8px;height:100px;
           background:#64c8ff;transition:left 30ms linear}
    </style>
    <div id='wrap'><div id='bar'></div></div>
    """
    area = st.empty()
    area.markdown(block, unsafe_allow_html=True)

    js = f"""
    <script>
      const bar=document.getElementById('bar'),
            wrap=document.getElementById('wrap');
      let pos=0, dir=1,
          px=(wrap.clientWidth-8)/({cycle_sec}*20);
      function step(){{
        pos += dir*px;
        if(pos<=0||pos>=wrap.clientWidth-8) dir*=-1;
        bar.style.left = pos + 'px';
      }}
      let t=setInterval(step,50);
      setTimeout(()=>clearInterval(t), {total_sec*1000});
    </script>
    """
    area.markdown(js, unsafe_allow_html=True)

if start_btn:
    emdr_session(minutes*60, cycle)
    st.success("Sesión terminada")
