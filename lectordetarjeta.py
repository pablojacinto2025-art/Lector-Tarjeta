import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Terminal Cyber", layout="centered", initial_sidebar_state="collapsed")

# Estilos visuales
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
            margin-bottom: 20px;
        }
        .stButton>button {
            width: 100%;
            background-color: #003b46;
            color: #00ffcc;
            border: 1px solid #00ffcc;
            font-weight: bold;
            height: 3.2em;
            border-radius: 5px;
            margin-top: 10px;
        }
        .stButton>button:hover {
            background-color: #07575b;
            color: #ffffff;
            border-color: #66fcf1;
        }
        .mensaje-espera {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 70vh;
            font-size: 2.3em;
            color: #00ffcc;
            font-weight: bold;
            letter-spacing: 2px;
            text-shadow: 0 0 15px rgba(0, 255, 204, 0.7);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Contraseñas asignadas por entidad
PIN_CONFIG = {
    "BCP": "1234",
    "InterBank": "4321",
    "BBVA": "1123"
}

# Inicialización de variables de estado
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"
if "banco_seleccionado" not in st.session_state:
    st.session_state.banco_seleccionado = "BCP"

# ==========================================
# 1. PANTALLA INICIAL: SELECCIÓN DE BANCO
# ==========================================
if st.session_state.etapa == "inicio":
    st.markdown("<h2 style='text-align: center; color: #00ffcc; margin-top: 40px;'>SISTEMA DE ACCESO</h2>", unsafe_allow_html=True)
    st.write("")
    
    if st.button("BCP"):
        st.session_state.banco_seleccionado = "BCP"
        st.session_state.etapa = "insertar"
        st.rerun()

    if st.button("InterBank"):
        st.session_state.banco_seleccionado = "InterBank"
        st.session_state.etapa = "insertar"
        st.rerun()

    if st.button("BBVA"):
        st.session_state.banco_seleccionado = "BBVA"
        st.session_state.etapa = "insertar"
        st.rerun()

# ==========================================
# 2. PANTALLA: SOLO "INSERTAR TARJETA" (10s)
# ==========================================
elif st.session_state.etapa == "insertar":
    pantalla_espera = st.empty()
    pantalla_espera.markdown("<div class='mensaje-espera'>INSERTAR TARJETA</div>", unsafe_allow_html=True)
    time.sleep(10)
    pantalla_espera.empty()
    st.session_state.etapa = "escaneando"
    st.rerun()

# ==========================================
# 3. PANTALLA: DETECCIÓN Y BUSCANDO DATOS
# ==========================================
elif st.session_state.etapa == "escaneando":
    banco_actual = st.session_state.banco_seleccionado

    st.markdown(f"""
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

    # El tipo toma automáticamente el nombre del banco pulsado
    logs = [
        f"// TIPO: DÉBITO {banco_actual}",
        "// EMV: ACTIVO",
        "// EXTRACCIÓN_VECTORS: [OK]",
        "// VERIFICANDO CLAVE DE AUTENTICACIÓN...",
        "// CARGANDO DATOS ENCRIPTADOS..."
    ]

    for p in range(1, 101):
        prog_bar.progress(p)
        status_txt.markdown(f"<h3 style='text-align:center; color:#00ffcc;'>BUSCANDO DATOS... [{p}%]</h3>", unsafe_allow_html=True)
        
        lineas = logs[:(p // 20) + 1]
        consola.markdown(
            f"<div style='background:#041014; padding:10px; border-left: 2px solid #00ffcc; font-size:0.85em; margin-top: 10px;'>"
            + "<br>".join(lineas) + 
            "</div>", 
            unsafe_allow_html=True
        )
        time.sleep(0.04)

    time.sleep(0.5)
    st.session_state.etapa = "password"
    st.rerun()

# ==========================================
# 4. PANTALLA: APARTADO DE CONTRASEÑA
# ==========================================
elif st.session_state.etapa == "password":
    banco_actual = st.session_state.banco_seleccionado

    st.markdown(f"""
        <div class='cyber-box'>
            <h3 style='text-align:center; color:#00ffcc; margin:0;'>AUTENTICACIÓN REQUERIDA</h3>
            <p style='text-align:center; font-size:0.9em; color:#80ced6; margin-top:8px;'>
                ENTIDAD SELECCIONADA: DÉBITO {banco_actual}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    pin = st.text_input("Ingresar contraseña (4 dígitos):", type="password", max_chars=4, placeholder="****")
    
    if st.button("INGRESAR"):
        clave_correcta = PIN_CONFIG.get(banco_actual)
        if pin == clave_correcta:
            st.success("ACCESO AUTORIZADO")
        else:
            st.error("CONTRASEÑA INCORRECTA")

    st.write("")
    if st.button("Cerrar Sesión"):
        st.session_state.etapa = "inicio"
        st.rerun()
