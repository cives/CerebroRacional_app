import streamlit as st
from openai import OpenAI
import json
import datetime

# Ejecutar con comando: streamlit run app.py

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Cerebro Externo 2e", page_icon="🧠", layout="wide")

# --- CSS PERSONALIZADO (Para estética "Hacker/Minimalista") ---
st.markdown("""
<style>
    .stButton>button {width: 100%; border-radius: 5px; height: 3em;}
    .big-font {font-size:20px !important;}
    div[data-testid="stMetricValue"] {font-size: 3rem;}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN BARRA LATERAL (Conexión OpenRouter) ---
with st.sidebar:
    st.title("⚙️ Configuración")
    
    # Input para tu API Key de OpenRouter
    api_key = st.text_input("OpenRouter API Key", type="password")
    
    # Selector de Modelo (Ventaja de OpenRouter: ¡Variedad!)
    model = st.selectbox(
        "Modelo de IA",
        ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash-exp:free"],
        index=1
    )
    
    st.divider()
    st.info("💡 Este sistema actúa como tu Lóbulo Frontal Prostético.")

# Inicializar cliente OpenAI apuntando a OpenRouter
if api_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
else:
    st.warning("⚠️ Por favor, introduce tu API Key en la barra lateral para activar la IA.")
    client = None

# --- GESTIÓN DE ESTADO (MEMORIA) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "black_box" not in st.session_state:
    st.session_state.black_box = ""

# --- NAVEGACIÓN ENTRE MÓDULOS ---
tabs = st.tabs(["🔨 Desatascador", "🍬 Menú Dopamina", "🚇 Modo Túnel", "🛡️ Coach Racional"])

# --- MÓDULO 1: EL DESATASCADOR (Goblin Tools) ---
with tabs[0]:
    st.header("🔨 El Desatascador de Tareas")
    st.caption("Rompe el monolito. Convierte lo imposible en pasos de 5 minutos.")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        task_input = st.text_input("¿En qué estás atascado?", placeholder="Ej: Limpiar el garaje...")
    with col2:
        break_down_btn = st.button("💥 Desglosar")

    if break_down_btn and client and task_input:
        with st.spinner("La IA está aplicando ingeniería inversa a tu tarea..."):
            try:
                prompt = f"Eres un experto en función ejecutiva. Desglosa la tarea '{task_input}' en micropasos extremadamente granulares (máximo 5 min cada uno). Devuelve solo una lista numerada, sin introducción ni conclusión."
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                steps = response.choices[0].message.content
                st.session_state['steps'] = steps
            except Exception as e:
                st.error(f"Error: {e}")

    if 'steps' in st.session_state:
        st.subheader("Tu Plan de Ataque:")
        # Renderizar pasos como lista de chequeo (Simulada visualmente)
        st.markdown(st.session_state['steps'])

# --- MÓDULO 2: MENÚ DE DOPAMINA ---
with tabs[1]:
    st.header("🍬 Menú de Dopamina")
    st.caption("Estimulación saludable a la carta. Carga tu batería ejecutiva.")
    
    # SECCIÓN 1: ENTRANTES (Energía Rápida - 5 min)
    st.subheader("🟢 Entrantes (Activación)")
    c1, c2, c3 = st.columns(3)
    
    if c1.button("💃 Bailar"): 
        st.toast("¡Movimiento activado! (Sube el volumen)")
        
    if c2.button("🎤 Cantar"): 
        st.toast("¡Liberando estrés! (A todo pulmón)")
        
    if c3.button("💧 Beber Agua"): 
        st.toast("¡Cerebro hidratado!")

    # SECCIÓN 2: PLATO FUERTE (Tus Intereses Reales)
    st.subheader("🟠 Plato Fuerte (Flujo Profundo)")
    c4, c5, c6 = st.columns(3)
    
    if c4.button("📚 Leer"): 
        st.success("¡Hora de viajar a otros mundos!")
    
    if c5.button("✍️ Escribir"): 
        st.success("¡Plasma tus ideas!")
        
    if c6.button("🎮 Jugar"): 
        st.success("¡Modo Estrategia activado!")
    
    # SECCIÓN 3: POSTRE (Recompensa Final)
    st.subheader("🔴 Postre (El Premio)")
    
    # Un botón grande para el premio final
    if st.button("🎬 Ver Serie / Película", type="primary"):
        st.balloons() # ¡Efecto de celebración visual!
        st.info("¡Disfruta! Te lo has ganado. (Recuerda poner una alarma de fin si tienes que madrugar).")    
    if st.button("📱 Redes Sociales (Bloqueado)"):
        st.error("⚠️ Espera... ¿Ya te comiste el plato fuerte? (Fricción añadida)")

# --- MÓDULO 3: MODO TÚNEL (Cockpit) ---
with tabs[2]:
    st.header("🚇 Cabina de Modo Túnel")
    
    col_dash1, col_dash2, col_dash3 = st.columns(3)
    with col_dash1:
        st.metric(label="Sesión Actual", value="Enfoque Profundo")
    with col_dash2:
        # Simulador de Timer Visual
        st.metric(label="Tiempo Restante", value="25:00", delta="-1 seg")
    with col_dash3:
        st.link_button("🎥 Entrar a Flown (Body Doubling)", "https://flown.com")

    st.divider()
    
    c_black1, c_black2 = st.columns([3, 1])
    with c_black1:
        st.subheader("📦 La Caja Negra")
        st.caption("Vomita aquí tus distracciones para no perder el foco. Se guardarán al final.")
        black_box_input = st.text_area("Captura rápida:", height=150, key="caja_negra_input")
    
    with c_black2:
        st.subheader("🚨 Pánico")
        if st.button("HARD BLOCK", type="primary"):
            st.warning("¡Modo Bloqueo Activado! Internet restringido.")

# --- MÓDULO 4: COACH RACIONAL (RSD) ---
with tabs[3]:
    st.header("🛡️ Arquitecto Racional")
    st.caption("Lógica sobre emoción. Reencuadre de datos.")

    # Historial de Chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input de Chat
    if prompt := st.chat_input("Reporte de estado emocional/ejecutivo..."):
        # Guardar y mostrar mensaje usuario
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lógica del Bot Racional
        if client:
            with st.chat_message("assistant"):
                system_prompt = "Eres un Arquitecto Racional. Tu usuario tiene TDAH y altas capacidades. Cuando el usuario exprese vergüenza o fallo, reencuadra la situación puramente como datos objetivos. Usa lógica, sé breve y ofrece una solución de fricción mínima. No uses tono condescendiente ni excesivamente emocional."
                stream = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": system_prompt}] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat_history
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.chat_history.append({"role": "assistant", "content": response})