import streamlit as st
import time

# Configuración móvil / pantalla completa
st.set_page_config(page_title="Terminal Cyber", layout="centered", initial_sidebar_state="collapsed")

# Estilos visuales oscuros y futuristas
st.markdown("""
    <style>
        .stApp {
            background-color: #0b1118;
            color: #00ffcc;
            font-family: 'Courier New', Courier, monospace;
        }
        .cyber-box {
            border: 2px solid #00ffcc;
            padding: 18px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.25);
            background-color: rgba(6, 26, 35, 0.85);
            margin-top: 15px;
        }
        .stButton>button {
            width: 100%;
            background-color: #003b46;
            color: #00ffcc;
            border: 1px solid #00ffcc;
            font-weight: bold;
            height: 3em;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #07575b;
            color: #ffffff;
            border-color: #66fcf1;
        }
    </style>
""", unsafe_allow_html=True)

# Lista de 4 contraseñas válidas de 4 dígitos
VALID_PINS = ["1234", "4321", "8888", "2026"]

# Inicializar estados
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"

# PANTALLA 1: Botón inicial
if st.session_state.etapa == "inicio":
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>SISTEMA DE ACCESO</h2>", unsafe_allow_html=True)
    if st.button("INICIAR PROTOCOLO"):
        st.session_state.etapa = "esperando"
        st.rerun()

# PANTALLA 2: Conteo regresivo de 10 segundos
elif st.session_state.etapa == "esperando":
    st.markdown("<h3 style='text-align: center;'>ESTABLECIENDO CONEXIÓN SEGURA...</h3>", unsafe_allow_html=True)
    barra = st.progress(0)
    tiempo_texto = st.empty()
    
    for i in range(10, 0, -1):
        tiempo_texto.markdown(f"<p style='text-align:center;'>Tiempo restante: {i}s</p>", unsafe_allow_html=True)
        barra.progress((10 - i + 1) * 10)
        time.sleep(1)
        
    st.session_state.etapa = "login"
    st.rerun()

# PANTALLA 3: Ingreso de PIN
elif st.session_state.etapa == "login":
    st.markdown("""
        <div class='cyber-box'>
            <h3 style='margin-top:0; text-align:center;'>INGRESAR CONTRASEÑA</h3>
            <p style='font-size: 0.85em; text-align:center; color: #80ced6;'>INTRODUZCA CÓDIGO DE ACCESO (4 DÍGITOS)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    pin = st.text_input("PIN:", type="password", max_chars=4, placeholder="****")
    
    if st.button("INGRESAR"):
        if pin in VALID_PINS:
            st.session_state.etapa = "escaneando"
            st.rerun()
        else:
            st.error("ACCESO DENEGADO: CÓDIGO INVÁLIDO")

# PANTALLA 4: Animación estilo terminal (HUD del video)
elif st.session_state.etapa == "escaneando":
    st.markdown("""
        <div class='cyber-box'>
            <div style='display: flex; justify-content: space-between; font-size: 0.8em; border-bottom: 1px solid #00ffcc; padding-bottom: 5px;'>
                <span>DISPOSITIVO: LECTOR_FÍSICO_01</span>
                <span>PUERTO: USB_C</span>
            </div>
            <h2 style='text-align: center; color: #00ffcc; margin: 15px 0 5px 0;'>TARJETA DETECTADA</h2>
        </div>
    """, unsafe_allow_html=True)

    status_txt = st.empty()
    prog_bar = st.progress(0)
    consola = st.empty()

    # Simulación de lectura de datos
    logs = [
        "// TIPO: DÉBITO MASTER",
        "// EMV: ACTIVO",
        "// EXTRACCIÓN_VECTORS: [OK]",
        "// VERIFICANDO CLAVE DE AUTENTICACIÓN...",
        "// CARGANDO DATOS ENCRIPTADOS..."
    ]

    for p in range(1, 101):
        prog_bar.progress(p)
        status_txt.markdown(f"<h3 style='text-align:center; color:#00ffcc;'>BUSCANDO DATOS... [{p}%]</h3>", unsafe_allow_html=True)
        
        # Muestra logs secuenciales conforme avanza la barra
        lineas_visibles = logs[:(p // 20) + 1]
        consola.markdown(
            f"<div style='background:#041014; padding:10px; border-left: 2px solid #00ffcc; font-size:0.85em;'>"
            + "<br>".join(lineas_visibles) + 
            "</div>", 
            unsafe_allow_html=True
        )
        time.sleep(0.04)

    st.success("DATOS DESCRIPTADOS EXITOSAMENTE")
    if st.button("REINICIAR"):
        st.session_state.etapa = "inicio"
        st.rerun()