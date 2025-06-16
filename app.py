import streamlit as st
import json

st.set_page_config(page_title="Listado de Precios", layout="wide")

# Función para cargar datos
def cargar_datos():
    with open("precios.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Login
st.title("Acceso al Listado de Precios")
tipo_usuario = st.radio("Tipo de acceso", ["Colaborador", "Administrador"])
clave = st.text_input("Clave", type="password")

if (tipo_usuario == "Colaborador" and clave == "invitado") or (tipo_usuario == "Administrador" and clave == "7852369"):
    datos = cargar_datos()
    if tipo_usuario == "Administrador":
        st.success("Acceso como ADMINISTRADOR")
    else:
        st.success("Acceso como COLABORADOR")

    proveedores = sorted(set([d["proveedor"] for d in datos]))
    proveedor_sel = st.selectbox("Filtrar por proveedor", ["Todos"] + proveedores)

    filtro = [d for d in datos if proveedor_sel == "Todos" or d["proveedor"] == proveedor_sel]

    st.write("Listado de precios:")
    st.dataframe(filtro, use_container_width=True)
else:
    st.warning("Introduce la clave correcta para acceder.")

