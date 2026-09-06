import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Terminal Cyber", layout="centered", initial_sidebar_state="collapsed")

# Estilos visuales con animaciones
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
            margin-top: 8px;
        }
        .stButton>button:hover {
            background-color: #07575b;
            color: #ffffff;
            border-color: #66fcf1;
        }
        
        /* Animación moderna para INSERTAR TARJETA */
        @keyframes pulso-neon {
            0%, 100% {
                box-shadow: 0 0 15px rgba(0, 255, 204, 0.4), inset 0 0 10px rgba(0, 255, 204, 0.2);
                border-color: #00ffcc;
                transform: scale(1);
            }
            50% {
                box-shadow: 0 0 30px rgba(0, 255, 204, 0.85), inset 0 0 20px rgba(0, 255, 204, 0.4);
                border-color: #66fcf1;
                transform: scale(1.02);
            }
        }
        @keyframes parpadeo-flecha {
            0%, 100% { opacity: 0.2; transform: translateY(0); }
            50% { opacity: 1; transform: translateY(8px); }
        }
        .contenedor-espera {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 65vh;
        }
        .caja-insertar {
            border: 2px solid #00ffcc;
            background: rgba(4, 16, 20, 0.85);
            border-radius: 12px;
            padding: 30px 40px;
            text-align: center;
            animation: pulso-neon 2s infinite ease-in-out;
        }
        .texto-insertar {
            font-size: 2.1em;
            font-weight: bold;
            letter-spacing: 3px;
            color: #00ffcc;
            text-shadow: 0 0 12px rgba(0, 255, 204, 0.8);
            margin: 0;
        }
        .ranura-tarjeta {
            width: 170px;
            height: 8px;
            background: #00222b;
            border: 1px solid #00ffcc;
            border-radius: 4px;
            margin: 20px auto 10px auto;
            box-shadow: 0 0 10px rgba(0,255,204,0.6);
        }
        .flecha-animada {
            font-size: 1.8em;
            color: #00ffcc;
            animation: parpadeo-flecha 1.2s infinite ease-in-out;
            margin-top: 5px;
        }

        /* Estilos de la tarjeta plástica */
        .tarjeta-plastica {
            width: 320px;
            height: 190px;
            margin: 20px auto 25px auto;
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            border: 1px solid rgba(255,255,255,0.2);
            box-sizing: border-box;
        }
        .tarjeta-bcp {
            background: linear-gradient(135deg, #0d2870 0%, #20418c 45%, #d95e00 100%);
        }
        .tarjeta-interbank {
            background: linear-gradient(135deg, #008f39 0%, #005f24 100%);
        }
        .tarjeta-bbVA {
            background: linear-gradient(135deg, #002e6e 0%, #004481 60%, #0066cc 100%);
        }
        .chip {
            width: 42px;
            height: 30px;
            background: linear-gradient(135deg, #e5b300, #ffde59);
            border-radius: 5px;
            border: 1px solid #b38b00;
        }
        .tarjeta-numero {
            font-size: 1.15em;
            letter-spacing: 3px;
            font-family: monospace;
            white-space: nowrap;
            display: block;
            margin-top: 8px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }
        .saldo-box {
            text-align: center;
            padding: 25px;
            background: rgba(6, 26, 35, 0.85);
            border: 2px solid #00ffcc;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Saldos y configuraciones
CONFIG_BANCOS = {
    "BCP": {
        "pin": "1234",
        "saldo": "S/ 3,438.17",
        "clase": "tarjeta-bcp"
    },
    "InterBank": {
        "pin": "4321",
        "saldo": "S/ 1,823.49",
        "clase": "tarjeta-interbank"
    },
    "BBVA": {
        "pin": "1123",
        "saldo": "S/ 5,078.83",
        "clase": "tarjeta-bbVA"
    }
}

# Inicialización de estados
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"
if "banco_seleccionado" not in st.session_state:
    st.session_state.banco_seleccionado = "BCP"

# Render de la tarjeta con asteriscos en una sola línea
def renderizar_tarjeta(banco):
    clase = CONFIG_BANCOS[banco]["clase"]
    return f"""
        <div class='tarjeta-plastica {clase}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:1.4em; font-weight:bold; letter-spacing:1px;'>{banco}</span>
                <span style='font-size:0.8em; opacity:0.9; font-weight:600;'>DÉBITO</span>
            </div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='chip'></div>
                <span style='font-size:0.75em; opacity:0.85;'>VAL 09/28</span>
            </div>
            <div>
                <span class='tarjeta-numero'>**** &nbsp;**** &nbsp;**** &nbsp;5892</span>
            </div>
        </div>
    """

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
# 2. PANTALLA: INSERTAR TARJETA (ANIMACIÓN Y PULSO)
# ==========================================
elif st.session_state.etapa == "insertar":
    pantalla_espera = st.empty()
    pantalla_espera.markdown("""
        <div class='contenedor-espera'>
            <div class='caja-insertar'>
                <div class='flecha-animada'>▼</div>
                <div class='ranura-tarjeta'></div>
                <h1 class='texto-insertar'>INSERTAR TARJETA</h1>
                <p style='color: #80ced6; font-size: 0.85em; margin-top: 15px; letter-spacing: 1px;'>
                    ESPERANDO DISPOSITIVO FÍSICO...
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(10)
    pantalla_espera.empty()
    st.session_state.etapa = "escaneando"
    st.rerun()

# ==========================================
# 3. PANTALLA: DETECCIÓN Y BUSCANDO DATOS
# ==========================================
elif st.session_state.etapa == "escaneando":
    banco = st.session_state.banco_seleccionado

    st.markdown(f"""
        <div class='cyber-box'>
            <div style='display: flex; justify-content: space-between; font-size: 0.8em; border-bottom: 1px solid #00ffcc; padding-bottom: 5px;'>
                <span>DISPOSITIVO: LECTOR_FÍSICO_01</span>
                <span>PUERTO: USB_C</span>
            </div>
            <h2 style='text-align: center; color: #00ffcc; margin: 15px 0 5px 0;'>TARJETA DETECTADA</h2>
            {renderizar_tarjeta(banco)}
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
# 4. PANTALLA: APARTADO DE CONTRASEÑA
# ==========================================
elif st.session_state.etapa == "password":
    banco = st.session_state.banco_seleccionado

    st.markdown(renderizar_tarjeta(banco), unsafe_allow_html=True)
    
    pin = st.text_input("Ingresar contraseña (4 dígitos):", type="password", max_chars=4, placeholder="****")
    
    if st.button("INGRESAR"):
        clave_correcta = CONFIG_BANCOS[banco]["pin"]
        if pin == clave_correcta:
            st.session_state.etapa = "saldo"
            st.rerun()
        else:
            st.error("CONTRASEÑA INCORRECTA")

    st.write("")
    if st.button("Cerrar Sesión"):
        st.session_state.etapa = "inicio"
        st.rerun()

# ==========================================
# 5. PANTALLA: SALDO CON BOTONES CONTINUAR / CERRAR
# ==========================================
elif st.session_state.etapa == "saldo":
    banco = st.session_state.banco_seleccionado
    monto_saldo = CONFIG_BANCOS[banco]["saldo"]

    st.markdown(renderizar_tarjeta(banco), unsafe_allow_html=True)

    st.markdown(f"""
        <div class='saldo-box'>
            <p style='color: #80ced6; font-size: 0.95em; letter-spacing: 1px; margin-bottom: 5px;'>SALDO DISPONIBLE</p>
            <h1 style='color: #00ffcc; margin: 0; font-size: 2.4em;'>{monto_saldo}</h1>
            <p style='color: #80ced6; font-size: 0.8em; margin-top: 8px;'>CUENTA EN SOLES - {banco}</p>
        </div>
    """, unsafe_allow_html=True)

    # Botón Continuar (vuelve al menú inicial)
    if st.button("CONTINUAR"):
        st.session_state.etapa = "inicio"
        st.rerun()

    if st.button("Cerrar Sesión"):
        st.session_state.etapa = "inicio"
        st.rerun()
