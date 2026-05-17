import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.logic import buscar_por_especie

st.set_page_config(page_title="Buscador de Mascotas", page_icon="🐾", layout="centered")

st.title("🐾 Buscador Semántico de Mascotas")
st.write("Escribe el nombre de una especie (ej. Perro, Gato) para ver las razas y mascotas registradas en nuestra Ontología.")

busqueda_usuario = st.text_input("🔍 Buscar por Especie (ej. Perro):")

if busqueda_usuario:
    try:
        resultados = buscar_por_especie(busqueda_usuario)
        
        if resultados:
            st.success(f"¡Encontramos {len(resultados)} resultados para '{busqueda_usuario}'!")
            df = pd.DataFrame(resultados)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No se encontraron mascotas para esa especie. ¡Intenta con otra!")
    except FileNotFoundError:
        st.error("No se encontró el archivo 'mascotas.owl'. Asegúrate de que el archivo existe en la raíz del proyecto.")
    except Exception as e:
        st.error(f"Error: {e}")