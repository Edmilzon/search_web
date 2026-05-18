import streamlit as st
import pandas as pd
import os


def inject_bootstrap():
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)
    
    styles_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "main.css")
    if os.path.exists(styles_path):
        with open(styles_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_results(resultados, titulo: str = "Resultados"):
    inject_bootstrap()
    
    df = pd.DataFrame(resultados)
    
    # Agregar badges según contenido
    if 'Raza' in df.columns:
        df['Tipo'] = df['Raza'].apply(lambda x: 
            '<span class="badge badge-perro">🐕 Perro</span>' if any(p in str(x).lower() for p in ['labrador', 'bulldog', 'pastor', 'golden', 'poodle', 'chihuahua', 'beagle', 'rottweiler', 'yorkshire', 'boxer', 'doberman', 'husky', 'shih tzu', 'border', 'collie']) 
            else ('<span class="badge badge-gato">🐈 Gato</span>' if any(g in str(x).lower() for g in ['persa', 'siamés', 'maine', 'bengala', 'ragdoll', 'british', 'esfinge', 'azul', 'abisinio', 'scottish', 'angora', 'savannah', 'bombay', 'noruego', 'birmano', 'akita'])
            else '')
        )
    
    html = df.to_html(classes='table table-custom', index=False, escape=False)
    st.markdown(html, unsafe_allow_html=True)


def render_results_raza(resultados):
    inject_bootstrap()
    
    df = pd.DataFrame(resultados)
    
    # Badge según especie
    if 'Especie' in df.columns:
        df['Badge'] = df['Especie'].apply(lambda x: 
            '<span class="badge badge-perro">🐕</span>' if 'Perro' in str(x) 
            else '<span class="badge badge-gato">🐈</span>'
        )
    
    html = df.to_html(classes='table table-custom', index=False, escape=False)
    st.markdown(html, unsafe_allow_html=True)


def render_error(mensaje: str):
    inject_bootstrap()
    st.markdown(f"""
    <div class="alert alert-danger alert-custom" role="alert">
        <i class="bi bi-exclamation-triangle-fill"></i> {mensaje}
    </div>
    """, unsafe_allow_html=True)


def render_warning(mensaje: str):
    inject_bootstrap()
    st.markdown(f"""
    <div class="alert alert-warning alert-custom" role="alert">
        <i class="bi bi-exclamation-circle-fill"></i> {mensaje}
    </div>
    """, unsafe_allow_html=True)


def render_success(mensaje: str):
    inject_bootstrap()
    st.markdown(f"""
    <div class="alert alert-success alert-custom" role="alert">
        <i class="bi bi-check-circle-fill"></i> {mensaje}
    </div>
    """, unsafe_allow_html=True)


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