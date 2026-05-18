import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.logic import buscar, get_todas, get_perros, get_gatos, get_razas
from backend.consultas import get_info_completa_perros, get_info_completa_gatos
from frontend.components import render_results, render_results_raza, render_error, render_warning, render_success


def main():
    st.set_page_config(
        page_title="Buscador de Mascotas",
        page_icon="🐾",
        layout="wide"
    )

    st.title("🐾 Buscador Semántico de Mascotas")
    st.markdown("""
    🔍 **Buscar por:** nombre, raza, especie (perro/gato), nombre del dueño, 
    marca de alimento, accesorio, tipo de pelaje
    """)

    menu = st.radio(
        "Navegación:",
        ["🏠 Inicio", "🐕 Perros", "🐈 Gatos", "🔍 Búsqueda", "📋 Razas"],
        horizontal=True
    )

    st.divider()

    if menu == "🏠 Inicio":
        render_inicio()
    elif menu == "🐕 Perros":
        render_perros()
    elif menu == "🐈 Gatos":
        render_gatos()
    elif menu == "🔍 Búsqueda":
        render_buscar()
    elif menu == "📋 Razas":
        render_razas()


def render_inicio():
    st.header("🐾 Todas las Mascotas")
    st.markdown("Bienvenido al buscador semántico de mascotas. Usa el menú superior para navegar.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🐾 Ver Todas las Mascotas", use_container_width=True):
            st.session_state.ver = "todas"
    with col2:
        if st.button("🐕 Ver Perros", use_container_width=True):
            st.session_state.ver = "perros"
    with col3:
        if st.button("🐈 Ver Gatos", use_container_width=True):
            st.session_state.ver = "gatos"
    
    st.divider()
    
    busqueda = st.text_input(
        "🔍 Buscar:",
        placeholder="Ej: Bobby, Labrador, Perro, Gato...",
        label_visibility="collapsed"
    )
    
    if busqueda:
        try:
            resultados = buscar(busqueda)
            if resultados:
                render_success(f"Se encontraron {len(resultados)} resultado(s) para '{busqueda}'")
                render_results(resultados, busqueda)
            else:
                render_warning(f"No se encontraron resultados para '{busqueda}'")
        except Exception as e:
            render_error(f"Error: {e}")
    elif "ver" in st.session_state:
        ver = st.session_state.ver
        try:
            if ver == "todas":
                resultados = get_todas()
                render_success(f"Todas las mascotas ({len(resultados)} encontradas)")
            elif ver == "perros":
                resultados = get_perros()
                render_success(f"Perros ({len(resultados)} encontrados)")
            elif ver == "gatos":
                resultados = get_gatos()
                render_success(f"Gatos ({len(resultados)} encontrados)")
            
            if resultados:
                render_results(resultados, ver)
            else:
                render_warning("No hay datos disponibles")
        except Exception as e:
            render_error(f"Error: {e}")


def render_perros():
    st.header("🐕 Perros")
    
    tab1, tab2 = st.tabs(["📋 Lista de Perros", "📊 Información Completa"])
    
    with tab1:
        try:
            resultados = get_perros()
            render_success(f"Se encontraron {len(resultados)} perros")
            if resultados:
                render_results(resultados, "perros")
            else:
                render_warning("No hay perros en la base de datos")
        except Exception as e:
            render_error(f"Error: {e}")
    
    with tab2:
        try:
            resultados = get_info_completa_perros()
            render_success(f"Se encontraron {len(resultados)} perros")
            if resultados:
                render_results(resultados, "info_perros")
            else:
                render_warning("No hay perros en la base de datos")
        except Exception as e:
            render_error(f"Error: {e}")


def render_gatos():
    st.header("🐈 Gatos")
    
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Gatos", "📊 Información Completa", "🐈 Sin Dueño"])
    
    with tab1:
        try:
            resultados = get_gatos()
            render_success(f"Se encontraron {len(resultados)} gatos")
            if resultados:
                render_results(resultados, "gatos")
            else:
                render_warning("No hay gatos en la base de datos")
        except Exception as e:
            render_error(f"Error: {e}")
    
    with tab2:
        try:
            resultados = get_info_completa_gatos()
            render_success(f"Se encontraron {len(resultados)} gatos")
            if resultados:
                render_results(resultados, "info_gatos")
            else:
                render_warning("No hay gatos en la base de datos")
        except Exception as e:
            render_error(f"Error: {e}")
    
    with tab3:
        from backend.consultas.gatos import get_gatos_sin_dueno
        try:
            resultados = get_gatos_sin_dueno()
            render_success(f"Se encontraron {len(resultados)} gatos sin dueño")
            if resultados:
                render_results(resultados, "sin_dueño")
            else:
                render_warning("No hay gatos sin dueño")
        except Exception as e:
            render_error(f"Error: {e}")


def render_buscar():
    st.header("🔍 Búsqueda Avanzada")
    
    busqueda = st.text_input(
        "🔍 Buscar:",
        placeholder="Ej: Bobby, Labrador, Perro, Gato, Carlos, Purina, Collar...",
        label_visibility="collapsed"
    )
    
    if busqueda:
        try:
            resultados = buscar(busqueda)
            if resultados:
                render_success(f"Se encontraron {len(resultados)} resultado(s) para '{busqueda}'")
                render_results(resultados, busqueda)
            else:
                render_warning(f"No se encontraron resultados para '{busqueda}'")
        except Exception as e:
            render_error(f"Error: {e}")
    else:
        render_warning("Escribe un término de búsqueda")


def render_razas():
    st.header("📋 Razas")
    
    try:
        resultados = get_razas()
        render_success(f"Se encontraron {len(resultados)} razas")
        if resultados:
            render_results_raza(resultados)
        else:
            render_warning("No hay razas en la base de datos")
    except Exception as e:
        render_error(f"Error: {e}")


if __name__ == "__main__":
    main()