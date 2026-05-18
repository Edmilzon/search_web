import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.logic import buscar, get_todas, get_perros, get_gatos, get_razas
from backend.consultas import get_info_completa_perros, get_info_completa_gatos
from frontend.components import render_results, render_results_raza, render_error, render_warning, render_success


def inject_bootstrap():
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)
    
    import os
    css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    inject_bootstrap()
    
    st.set_page_config(
        page_title="🐾 Buscador de Mascotas",
        page_icon="🐾",
        layout="wide"
    )

    # Navbar
    st.markdown("""
    <nav class="navbar-custom">
        <div class="container">
            <div class="d-flex align-items-center justify-content-between w-100">
                <span class="navbar-brand">
                    <i class="bi bi-paw"></i> Buscador Semántico de Mascotas
                </span>
                <span class="navbar-text">
                    🔍 Búsqueda Inteligente
                </span>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    # Menu de navegación
    col_menu = st.columns([1, 1, 1, 1, 1])
    with col_menu[0]:
        st.markdown('<a class="menu-btn active" href="#">🏠 Inicio</a>', unsafe_allow_html=True)
    with col_menu[1]:
        st.markdown('<a class="menu-btn" href="#perros">🐕 Perros</a>', unsafe_allow_html=True)
    with col_menu[2]:
        st.markdown('<a class="menu-btn" href="#gatos">🐈 Gatos</a>', unsafe_allow_html=True)
    with col_menu[3]:
        st.markdown('<a class="menu-btn" href="#buscar">🔍 Búsqueda</a>', unsafe_allow_html=True)
    with col_menu[4]:
        st.markdown('<a class="menu-btn" href="#razas">📋 Razas</a>', unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # Menú lateral
    menu = st.radio(
        "Navegación:",
        ["🏠 Inicio", "🐕 Perros", "🐈 Gatos", "🔍 Búsqueda", "📋 Razas"],
        horizontal=True,
        label_visibility="collapsed"
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
    # Stats
    try:
        todas = get_todas()
        perros = get_perros()
        gatos = get_gatos()
        
        col_stats = st.columns(4)
        with col_stats[0]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(todas)}</div>
                <div class="stat-label">🐾 Total Mascotas</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[1]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(perros)}</div>
                <div class="stat-label">🐕 Perros</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[2]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(gatos)}</div>
                <div class="stat-label">🐈 Gatos</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[3]:
            try:
                razas = get_razas()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(razas)}</div>
                    <div class="stat-label">🐶 Razas</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown("""
                <div class="stat-card">
                    <div class="stat-number">30</div>
                    <div class="stat-label">🐶 Razas</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> Error al cargar estadísticas: {e}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔍 Buscar Mascotas", unsafe_allow_html=True)
    
    # Search
    busqueda = st.text_input(
        "Buscar:",
        placeholder="🔍 Busca por nombre, raza, especie, dueño, alimento...",
        label_visibility="collapsed",
        key="busqueda_inicio"
    )

    if busqueda:
        try:
            resultados = buscar(busqueda)
            if resultados:
                st.markdown(f"""
                <div class="alert alert-success-custom alert-custom">
                    <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} resultado(s) para "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
                render_results(resultados, busqueda)
            else:
                st.markdown(f"""
                <div class="alert alert-warning-custom alert-custom">
                    <i class="bi bi-exclamation-circle-fill"></i> No se encontraron resultados para "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)


def render_perros():
    st.markdown("## 🐕 Perros", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Lista de Perros", "📊 Información Completa"])
    
    with tab1:
        try:
            resultados = get_perros()
            st.markdown(f"""
            <div class="alert alert-success-custom alert-custom">
                <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} perros
            </div>
            """, unsafe_allow_html=True)
            if resultados:
                render_results(resultados, "perros")
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        try:
            resultados = get_info_completa_perros()
            st.markdown(f"""
            <div class="alert alert-success-custom alert-custom">
                <i class="bi bi-check-circle-fill"></i> Información completa de {len(resultados)} perros
            </div>
            """, unsafe_allow_html=True)
            if resultados:
                render_results(resultados, "info_perros")
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)


def render_gatos():
    st.markdown("## 🐈 Gatos", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Gatos", "📊 Información Completa", "🐈 Sin Dueño"])
    
    with tab1:
        try:
            resultados = get_gatos()
            st.markdown(f"""
            <div class="alert alert-success-custom alert-custom">
                <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} gatos
            </div>
            """, unsafe_allow_html=True)
            if resultados:
                render_results(resultados, "gatos")
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        try:
            resultados = get_info_completa_gatos()
            st.markdown(f"""
            <div class="alert alert-success-custom alert-custom">
                <i class="bi bi-check-circle-fill"></i> Información completa de {len(resultados)} gatos
            </div>
            """, unsafe_allow_html=True)
            if resultados:
                render_results(resultados, "info_gatos")
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        from backend.consultas.gatos import get_gatos_sin_dueno
        try:
            resultados = get_gatos_sin_dueno()
            st.markdown(f"""
            <div class="alert alert-warning-custom alert-custom">
                <i class="bi bi-exclamation-circle-fill"></i> Se encontraron {len(resultados)} gatos sin dueño
            </div>
            """, unsafe_allow_html=True)
            if resultados:
                render_results(resultados, "sin_dueño")
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)


def render_buscar():
    st.markdown("## 🔍 Búsqueda Avanzada", unsafe_allow_html=True)
    st.markdown("""
    <p class="text-muted">
    Busca por: <span class="text-accent">nombre</span>, 
    <span class="text-accent">raza</span>, 
    <span class="text-accent">especie</span> (perro/gato), 
    <span class="text-accent">nombre del dueño</span>, 
    <span class="text-accent">marca de alimento</span>, 
    <span class="text-accent">accesorio</span>, 
    <span class="text-accent">tipo de pelaje</span>
    </p>
    """, unsafe_allow_html=True)
    
    busqueda = st.text_input(
        "Buscar:",
        placeholder="🔍 Ej: Bobby, Labrador, Perro, Gato, Carlos, Purina, Collar...",
        label_visibility="collapsed",
        key="busqueda_avanzada"
    )
    
    if busqueda:
        try:
            resultados = buscar(busqueda)
            if resultados:
                st.markdown(f"""
                <div class="alert alert-success-custom alert-custom">
                    <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} resultado(s) para "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
                render_results(resultados, busqueda)
            else:
                st.markdown(f"""
                <div class="alert alert-warning-custom alert-custom">
                    <i class="bi bi-exclamation-circle-fill"></i> No se encontraron resultados para "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert alert-warning-custom alert-custom">
            <i class="bi bi-info-circle-fill"></i> Escribe un término de búsqueda
        </div>
        """, unsafe_allow_html=True)


def render_razas():
    st.markdown("## 📋 Razas", unsafe_allow_html=True)
    
    try:
        resultados = get_razas()
        st.markdown(f"""
        <div class="alert alert-success-custom alert-custom">
            <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} razas
        </div>
        """, unsafe_allow_html=True)
        if resultados:
            render_results_raza(resultados)
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()