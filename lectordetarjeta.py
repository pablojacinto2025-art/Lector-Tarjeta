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
            height: 3.2em;
            border-radius: 5px;
            margin-bottom: 8px;
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
            height: 50vh;
            font-size: 2.2em;
            color: #00ffcc;
            font-weight: bold;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.7);
        }
    </style>
""", unsafe_allow_html=True)

# Inicializar estados de sesión
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"
if "banco" not in st.session_state:
    st.session_state.banco = "BCP"

# PANTALLA 1: Selección entre 3 botones
if st.session_state.etapa == "inicio":
    st.markdown("<h2 style='text-align: center; color: #00ffcc; margin-top: 30px;'>SISTEMA DE ACCESO</h2>", unsafe_allow_html=True)
    st.write("")
    
    if st.button("BCP"):
        st.session_state.banco = "BCP"
        st.session_state.etapa = "insertar"
        st.rerun()

    if st.button("InterBank"):
        st.session_state.banco = "InterBank"
        st.session_state.etapa = "insertar"
        st.rerun()

    if st.button("BBVA"):
        st.session_state.banco = "BBVA"
        st.session_state.etapa = "insertar"
        st.rerun()

# PANTALLA 2: Espera de 10 segundos
elif st.session_state.etapa == "insertar":
    contenedor = st.empty()
    contenedor.markdown("<div class='mensaje-espera'>INSERTAR TARJETA</div>", unsafe_allow_html=True)
    time.sleep(10)
    st.session_state.etapa = "escaneando"
    st.rerun()

# PANTALLA 3: Tarjeta detectada con el banco seleccionado
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

    # Se adapta automáticamente al botón seleccionado
    logs = [
        f"// TIPO: DÉBITO {st.session_state.banco}",
        "// EMV: ACTIVO",
        "// EXTRACCIÓN_VECTORS: [OK]",
        "// VERIFICANDO CLAVE DE AUTENTICACIÓN...",
        "// CARGANDO DATOS ENCRIPTADOS..."
    ]

    for p in range(1, 101):
        prog_bar.progress(p)
        status_txt.markdown(f"<h3 style='text-align:center; color:#00ffcc;'>BUSCANDO DATOS... [{p}%]</h3>", unsafe_allow_html=True)
        
        lineas_visibles = logs[:(p // 20) + 1]
        consola.markdown(
            f"<div style='background:#041014; padding:10px; border-left: 2px solid #00ffcc; font-size:0.85em; margin-top: 10px;'>"
            + "<br>".join(lineas_visibles) + 
            "</div>", 
            unsafe_allow_html=True
        )
        time.sleep(0.04)

    st.write("")
    st.success("DATOS DESCRIPTADOS EXITOSAMENTE")
    if st.button("REINICIAR"):
        st.session_state.etapa = "inicio"
        st.rerun()
