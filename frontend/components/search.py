import streamlit as st
import pandas as pd


def render_search_bar():
    return st.text_input(
        "🔍 Buscar por Especie (ej. Perro, Gato):",
        placeholder="Ingresa el nombre de una especie..."
    )


def render_results(resultados, busqueda):
    df = pd.DataFrame(resultados)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nombre": st.column_config.TextColumn("🐾 Mascota", width="medium"),
            "Raza": st.column_config.TextColumn("🐶 Raza", width="medium"),
            "Edad": st.column_config.TextColumn("🎂 Edad", width="small"),
            "Peso": st.column_config.TextColumn("⚖️ Peso", width="small"),
            "Color": st.column_config.TextColumn("🎨 Color", width="small"),
            "Sexo": st.column_config.TextColumn("♂️ Sexo", width="small"),
            "Dueño": st.column_config.TextColumn("👤 Dueño", width="medium"),
            "Alimento": st.column_config.TextColumn("🍖 Alimento", width="medium"),
            "Tipo de Alimento": st.column_config.TextColumn("🍽️ Tipo", width="small"),
            "Accesorio": st.column_config.TextColumn("🎾 Accesorio", width="medium"),
            "Tipo de Pelaje": st.column_config.TextColumn("🧸 Pelaje", width="small"),
            "Tipo de Cuidado": st.column_config.TextColumn("✂️ Cuidado", width="small")
        }
    )


def render_results_raza(resultados):
    df = pd.DataFrame(resultados)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Raza": st.column_config.TextColumn("🐶 Raza", width="medium"),
            "Especie": st.column_config.TextColumn("🐾 Especie", width="medium"),
            "Mascotas": st.column_config.TextColumn("🐾 Mascotas", width="large")
        }
    )


def render_error(message):
    st.error(message)