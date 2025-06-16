import streamlit as st
import json

# Autenticación
st.sidebar.title("🔐 Acceso")
usuario = st.sidebar.text_input("Usuario")
clave = st.sidebar.text_input("Clave", type="password")

modo_admin = (usuario == "YHUERTA" and clave == "7852369")

# Cargar datos
with open("precios.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("📋 BIOCITRUS - Listado de Precios 📲")
categoria = st.selectbox("Selecciona una categoría", list(data.keys()))
busqueda = st.text_input("Buscar producto")

# Mostrar resultados
for producto in data.get(categoria, []):
    if busqueda.lower() in producto["producto"].lower():
        st.markdown(f"**{producto['producto']}**")
        st.write(f"Proveedor: {producto['proveedor']}")
        st.write(f"Activo: {producto['activo']}")
        st.write(f"Presentacion: {producto['presentacion']}")
        st.write(f"Precio: S/ {producto['precio']:.2f}")
        if modo_admin:
            st.info("Modo administrador activado")
        st.markdown("---")
