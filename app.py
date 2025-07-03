import streamlit as st
import json

st.set_page_config(page_title="📦 Listado de Precios", layout="wide")
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📦 Sistema de Precios</h1>", unsafe_allow_html=True)

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

# --- Acceso ---
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        tipo_usuario = st.radio("🔐 Tipo de acceso", ["Colaborador", "Administrador"])
    with col2:
        clave = st.text_input("🔑 Ingrese la clave", type="password")

acceso_concedido = False
if tipo_usuario and clave:
    if (tipo_usuario == "Colaborador" and clave == "91") or (tipo_usuario == "Administrador" and clave == "7852369"):
        acceso_concedido = True
    else:
        st.error("❌ Clave incorrecta.")
else:
    st.warning("⚠️ Debe ingresar una clave para continuar.")

# --- Contenido principal ---
if acceso_concedido:
    try:
        with open("precios.json", "r", encoding="utf-8") as f:
            productos = json.load(f)
    except:
        st.error("⚠️ Error al cargar el archivo de precios.")
        st.stop()

    # Ordenar productos alfabéticamente
    productos = sorted(productos, key=lambda x: x["producto"])

    st.markdown("### 🔍 Buscar productos")
    colf1, colf2 = st.columns([2, 3])
    with colf1:
        proveedores = sorted(set([p["proveedor"] for p in productos]))
        proveedor_sel = st.selectbox("Filtrar por proveedor", ["Todos"] + proveedores)
    with colf2:
        busqueda = st.text_input("Buscar por nombre o parte del producto").lower()

    resultados = [p for p in productos if (proveedor_sel == "Todos" or p["proveedor"] == proveedor_sel) and busqueda in p["producto"].lower()]
    st.markdown("### 📋 Resultados")
    st.dataframe(resultados, use_container_width=True)

    # --- Agregar producto ---
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
                precio = st.number_input("💲 Precio", min_value=0.0, step=0.1)
            submitted = st.form_submit_button("✅ Agregar producto")
            if submitted:
                nuevo = {
                    "producto": producto,
                    "proveedor": proveedor,
                    "activo": activo,
                    "categoria": categoria,
                    "presentacion": presentacion,
                    "precio": precio
                }
                productos.append(nuevo)
                with open("precios.json", "w", encoding="utf-8") as f:
                    json.dump(productos, f, indent=2, ensure_ascii=False)
                st.success("✅ Producto agregado exitosamente.")

        # --- Editar/Eliminar producto ---
        st.markdown("---")
        st.markdown("### ✏️ Editar o eliminar producto")
        nombres = [p["producto"] for p in productos]
        seleccionado = st.selectbox("Selecciona un producto para editar o eliminar", nombres)
        producto_sel = next((p for p in productos if p["producto"] == seleccionado), None)
        if producto_sel:
            with st.form("editar_producto"):
                col1, col2 = st.columns(2)
                with col1:
                    nuevo_producto = st.text_input("🧪 Producto", value=producto_sel["producto"])
                    nuevo_proveedor = st.text_input("🏭 Proveedor", value=producto_sel["proveedor"])
                    nuevo_activo = st.text_input("💊 Activo", value=producto_sel["activo"])
                with col2:
                    nueva_categoria = st.text_input("📂 Categoría", value=producto_sel["categoria"])
                    nueva_presentacion = st.text_input("📦 Presentación", value=producto_sel["presentacion"])
                    nuevo_precio = st.number_input("💲 Precio", value=producto_sel["precio"], min_value=0.0, step=0.1)
                col_ed1, col_ed2 = st.columns(2)
                guardar = col_ed1.form_submit_button("💾 Guardar cambios")
                eliminar = col_ed2.form_submit_button("🗑️ Eliminar producto")

                if guardar:
                    producto_sel.update({
                        "producto": nuevo_producto,
                        "proveedor": nuevo_proveedor,
                        "activo": nuevo_activo,
                        "categoria": nueva_categoria,
                        "presentacion": nueva_presentacion,
                        "precio": nuevo_precio
                    })
                    with open("precios.json", "w", encoding="utf-8") as f:
                        json.dump(productos, f, indent=2, ensure_ascii=False)
                    st.success("✅ Cambios guardados.")

                if eliminar:
                    productos.remove(producto_sel)
                    with open("precios.json", "w", encoding="utf-8") as f:
                        json.dump(productos, f, indent=2, ensure_ascii=False)
                    st.success("🗑️ Producto eliminado.")
