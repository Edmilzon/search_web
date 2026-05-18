import streamlit as st
import pandas as pd


def render_results(resultados, titulo: str = "Resultados"):
    df = pd.DataFrame(resultados)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config=render_column_config(df.columns.tolist())
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


def render_error(mensaje: str):
    st.error(mensaje)


def render_warning(mensaje: str):
    st.warning(mensaje)


def render_success(mensaje: str):
    st.success(mensaje)


def render_column_config(columnas: list):
    config = {}
    mapeo = {
        "nombre": ("🐾 Mascota", "medium"),
        "Nombre": ("🐾 Mascota", "medium"),
        "raza": ("🐶 Raza", "medium"),
        "Raza": ("🐶 Raza", "medium"),
        "edad": ("🎂 Edad", "small"),
        "Edad": ("🎂 Edad", "small"),
        "peso": ("⚖️ Peso", "small"),
        "Peso": ("⚖️ Peso", "small"),
        "color": ("🎨 Color", "small"),
        "Color": ("🎨 Color", "small"),
        "sexo": ("♂️ Sexo", "small"),
        "Sexo": ("♂️ Sexo", "small"),
        "dueño": ("👤 Dueño", "medium"),
        "Dueño": ("👤 Dueño", "medium"),
        "alimento": ("🍖 Alimento", "medium"),
        "Alimento": ("🍖 Alimento", "medium"),
        "tipo_alimento": ("🍽️ Tipo", "small"),
        "Tipo de Alimento": ("🍽️ Tipo", "small"),
        "accesorio": ("🎾 Accesorio", "medium"),
        "Accesorio": ("🎾 Accesorio", "medium"),
        "tipo_pelaje": ("🧸 Pelaje", "small"),
        "Tipo de Pelaje": ("🧸 Pelaje", "small"),
        "tipo_cuidado": ("✂️ Cuidado", "small"),
        "Tipo de Cuidado": ("✂️ Cuidado", "small"),
        "especie": ("🐾 Especie", "medium"),
        "Especie": ("🐾 Especie", "medium"),
        "mascotas": ("🐾 Mascotas", "large"),
        "Mascotas": ("🐾 Mascotas", "large")
    }
    for col in columnas:
        if col in mapeo:
            label, width = mapeo[col]
            config[col] = st.column_config.TextColumn(label, width=width)
    return config