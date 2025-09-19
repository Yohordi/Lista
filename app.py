import streamlit as st
import json
import pandas as pd
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="📦 Listado de Precios", layout="wide")
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📦 Sistema de Precios Biocitrus</h1>", unsafe_allow_html=True)

# --- Estilos personalizados ---
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        border: 1px solid #ccc;
        padding: 6px;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
        padding: 6px 12px;
        margin-top: 8px;
    }
    .stDataFrame {
        border: 1px solid #eee;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Control de sesión ---
if "logueado" not in st.session_state:
    st.session_state.logueado = False
    st.session_state.tipo_usuario = None

if not st.session_state.logueado:
    st.markdown("### 🔐 Iniciar sesión")
    col1, col2, col3 = st.columns([1.5, 2.5, 1])
    with col1:
        tipo_input = st.radio("Tipo de acceso", ["Colaborador", "Administrador"])
    with col2:
        clave = st.text_input("Ingrese la clave", type="password")
    with col3:
        if st.button("🔓 Acceder"):
            if (tipo_input == "Colaborador" and clave == "91") or (tipo_input == "Administrador" and clave == "7852369"):
                st.session_state.logueado = True
                st.session_state.tipo_usuario = tipo_input
                st.rerun()
            else:
                st.error("❌ Clave incorrecta.")
    st.stop()

st.markdown(f"👤 Bienvenido, **{st.session_state.tipo_usuario}**")
if st.button("🔒 Cerrar sesión"):
    st.session_state.logueado = False
    st.session_state.tipo_usuario = None
    st.rerun()

tipo_usuario = st.session_state.tipo_usuario

# --- Cargar productos ---
try:
    with open("precios.json", "r", encoding="utf-8") as f:
        productos = json.load(f)
except:
    st.error("⚠️ Error al cargar el archivo de precios.")
    st.stop()

productos = sorted(productos, key=lambda x: x["producto"])

# --- Filtros y búsqueda ---
st.markdown("### 🔍 Buscar productos")
colf1, colf2 = st.columns([2, 3])
with colf1:
    proveedores = sorted(set([p["proveedor"] for p in productos]))
    proveedor_sel = st.selectbox("Filtrar por proveedor", ["Todos"] + proveedores)
with colf2:
    busqueda = st.text_input("Buscar por nombre o parte del producto").lower()

resultados = [
    p for p in productos
    if (proveedor_sel == "Todos" or p["proveedor"] == proveedor_sel)
    and busqueda in p["producto"].lower()
]

# --- Mostrar resultados ---
if resultados:
    st.markdown("### 📋 **Precios**")
    df = pd.DataFrame(resultados)
    df.columns = [col.upper() for col in df.columns]

    # Estilos personalizados para tabla
    def style_table(df):
        styler = df.style.set_table_styles([
            {"selector": "thead th", "props": [
                ("background-color", "#f0f2f6"),
                ("color", "#2c3e50"),
                ("font-weight", "normal"),
                ("text-align", "center"),
                ("padding", "8px")
            ]},
            {"selector": "tbody td", "props": [
                ("text-align", "center"),
                ("padding", "6px"),
                ("font-size", "13px"),
                ("color", "#333")
            ]}
        ]).hide(axis="index")

        # Resaltar columnas específicas
        if "PRODUCTO" in df.columns:
            styler = styler.set_properties(subset=["PRODUCTO"], **{"color": "#1f77b4", "font-weight": "bold"})
        if "PRECIO" in df.columns:
            styler = styler.set_properties(subset=["PRECIO"], **{"color": "#27ae60", "font-weight": "bold"})
        if "PROVEEDOR" in df.columns:
            styler = styler.set_properties(subset=["PROVEEDOR"], **{"color": "#8e44ad"})

        return styler

    st.dataframe(style_table(df), use_container_width=True)
else:
    st.info("No se encontraron productos.")

# --- Si es administrador, mostrar panel de edición ---
if tipo_usuario == "Administrador":
    st.markdown("---")
    st.markdown("### ➕ Agregar nuevo producto")
    with st.form("nuevo_producto"):
        col1, col2 = st.columns(2)
        with col1:
            producto = st.text_input("🧪 Producto")
            proveedor = st.text_input("🏭 Proveedor")
            activo = st.text_input("💊 Activo (composición)")
        with col2:
            categoria = st.text_input("📂 Categoría")
            presentacion = st.text_input("📦 Presentación")
            precio = st.number_input("💲 Precio", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("✅ Agregar producto")
        if submitted:
            if producto and proveedor and activo and categoria and presentacion:
                nuevo = {
                    "producto": producto,
                    "proveedor": proveedor,
                    "activo": activo,
                    "categoria": categoria,
                    "presentacion": presentacion,
                    "precio": int(precio)
                }
                productos.append(nuevo)
                with open("precios.json", "w", encoding="utf-8") as f:
                    json.dump(productos, f, indent=2, ensure_ascii=False)
                st.success("✅ Producto agregado exitosamente.")
                st.rerun()
            else:
                st.warning("⚠️ Complete todos los campos.")

    st.markdown("---")
    st.markdown("### ✏️ Editar o eliminar producto")
    nombres = [p["producto"] for p in productos]
    seleccionado = st.selectbox("Selecciona un producto", nombres)
    producto_sel = next((p for p in productos if p["producto"] == seleccionado), None)
    if producto_sel:
        with st.form("editar_producto"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_producto = st.text_input("🧪 Producto", value=producto_sel["producto"])
                nuevo_proveedor = st.text_input("🏭 Proveedor", value=producto_sel["proveedor"])
                nuevo_activo = st.text_input("💊 Activo", value=producto_sel["activo"])

