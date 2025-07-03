import streamlit as st
import json

st.set_page_config(page_title="Listado de Precios", layout="wide")

st.title("📦 Listado de Precios")

# Acceso
tipo_usuario = st.radio("Tipo de acceso", ["Colaborador", "Administrador"])
clave = st.text_input("Ingrese la clave", type="password")

acceso_concedido = False
if tipo_usuario and clave:
    if (tipo_usuario == "Colaborador" and clave == "91") or (tipo_usuario == "Administrador" and clave == "7852369"):
        acceso_concedido = True
    else:
        st.error("Clave incorrecta.")
else:
    st.warning("Debe ingresar una clave para continuar.")

if acceso_concedido:
    try:
        with open("precios.json", "r", encoding="utf-8") as f:
            productos = json.load(f)
    except Exception as e:
        st.error("Error al cargar el archivo de precios.")
        st.stop()

    proveedores = sorted(set([p["proveedor"] for p in productos]))
    proveedor_sel = st.selectbox("Filtrar por proveedor", ["Todos"] + proveedores)

    busqueda = st.text_input("Buscar producto").lower()

    resultados = []
    for producto in productos:
        if (proveedor_sel == "Todos" or producto["proveedor"] == proveedor_sel) and            (busqueda in producto["producto"].lower()):
            resultados.append(producto)

    st.markdown("### Resultados")
    st.dataframe(resultados, use_container_width=True)

    if tipo_usuario == "Administrador":
        st.markdown("### Agregar nuevo producto")
        with st.form("nuevo_producto"):
            codigo = st.text_input("Código")
            producto = st.text_input("Producto")
            proveedor = st.text_input("Proveedor")
            activo = st.selectbox("¿Activo?", ["Sí", "No"])
            categoria = st.text_input("Categoría")
            presentacion = st.text_input("Presentación")
            precio = st.number_input("Precio", min_value=0.0, step=0.1)
            submitted = st.form_submit_button("Agregar")

            if submitted:
                nuevo = {
                    "codigo": codigo,
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
                st.success("Producto agregado exitosamente.")

