import streamlit as st


def render_search_input(placeholder: str = "Buscar...", label: str = "🔍 Buscar:"):
    return st.text_input(
        label,
        placeholder=placeholder,
        label_visibility="collapsed"
    )


def render_search_with_filters():
    col1, col2 = st.columns([3, 1])
    with col1:
        busqueda = st.text_input(
            "🔍 Buscar:",
            placeholder="Ej: Bobby, Labrador, Perro, Gato...",
            label_visibility="collapsed"
        )
    with col2:
        filtro = st.selectbox(
            "Filtrar por:",
            ["Todos", "Nombre", "Raza", "Especie", "Dueño", "Alimento"]
        )
    return busqueda, filtro