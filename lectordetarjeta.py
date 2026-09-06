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
        /* Estilos para la tarjeta plástica dinámica */
        .tarjeta-plastica {
            width: 290px;
            height: 175px;
            margin: 15px auto;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: white;
            font-family: Arial, sans-serif;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .tarjeta-bcp {
            background: linear-gradient(135deg, #002a8f, #ff7800);
        }
        .tarjeta-interbank {
            background: linear-gradient(135deg, #009944, #00552b);
        }
        .tarjeta-bbva {
            background: linear-gradient(135deg, #004481, #1464a5);
        }
        .chip {
            width: 38px;
            height: 28px;
            background: linear-gradient(135deg, #e6b800, #ffd700);
            border-radius: 4px;
            border: 1px solid #b38600;
        }
    </style>
""", unsafe_allow_html=True)

# Contraseñas configuradas
PIN_CONFIG = {
    "BCP": "1234",
    "InterBank": "4321",
    "BBVA": "1123"
}

# Inicializar variables
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
# 3. PANTALLA: DETECTANDO LA TARJETA SELECCIONADA
# ==========================================
elif st.session_state.etapa == "escaneando":
    banco = st.session_state.banco_seleccionado

    # Determinar la clase de color según el banco
    clase_tarjeta = "tarjeta-bbva"
    if banco == "BCP":
        clase_tarjeta = "tarjeta-bcp"
    elif banco == "InterBank":
        clase_tarjeta = "tarjeta-interbank"

    # Tarjeta gráfica en el centro que cambia según el banco
    tarjeta_html = f"""
        <div class='tarjeta-plastica {clase_tarjeta}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:1.3em; font-weight:bold; letter-spacing:1px;'>{banco}</span>
                <span style='font-size:0.75em; opacity:0.8;'>DÉBITO</span>
            </div>
            <div class='chip'></div>
            <div style='display:flex; justify-content:space-between; align-items:flex-end;'>
                <span style='font-size:0.9em; letter-spacing:2px; font-family:monospace;'>•••• •••• •••• 5892</span>
                <span style='font-size:0.75em;'>09/28</span>
            </div>
        </div>
    """

    st.markdown(f"""
        <div class='cyber-box'>
            <div style='display: flex; justify-content: space-between; font-size: 0.8em; border-bottom: 1px solid #00ffcc; padding-bottom: 5px;'>
                <span>DISPOSITIVO: LECTOR_FÍSICO_01</span>
                <span>PUERTO: USB_C</span>
            </div>
            <h2 style='text-align: center; color: #00ffcc; margin: 15px 0 5px 0;'>TARJETA DETECTADA</h2>
            {tarjeta_html}
        </div>
    """, unsafe_allow_html=True)

    status_txt = st.empty()
    prog_bar = st.progress(0)
    consola = st.empty()

    logs = [
        f"// TIPO: DÉBITO {banco}",
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
# 4. PANTALLA: APARTADO SOLO DE CONTRASEÑA
# ==========================================
elif st.session_state.etapa == "password":
    banco = st.session_state.banco_seleccionado

    st.markdown(f"""
        <div class='cyber-box'>
            <h3 style='text-align:center; color:#00ffcc; margin:0;'>AUTENTICACIÓN REQUERIDA</h3>
            <p style='text-align:center; font-size:0.9em; color:#80ced6; margin-top:8px;'>
                ENTIDAD SELECCIONADA: DÉBITO {banco}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    pin = st.text_input("Ingresar contraseña (4 dígitos):", type="password", max_chars=4, placeholder="****")
    
    if st.button("INGRESAR"):
        clave_correcta = PIN_CONFIG.get(banco)
        if pin == clave_correcta:
            st.success("ACCESO AUTORIZADO")
        else:
            st.error("CONTRASEÑA INCORRECTA")

    st.write("")
    if st.button("Cerrar Sesión"):
        st.session_state.etapa = "inicio"
        st.rerun()
