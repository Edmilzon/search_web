import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.logic import buscar, get_todas, get_perros, get_gatos, get_razas, get_contar_duenos
from backend.consultas import get_info_completa_perros, get_info_completa_gatos
from frontend.components import render_results, render_results_raza


def inject_bootstrap():
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    """, unsafe_allow_html=True)

    css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    inject_bootstrap()

    st.set_page_config(
        page_title="Buscador de Mascotas",
        page_icon=":dog:",
        layout="wide"
    )

    # Header
    st.markdown("""
    <nav class="navbar-custom">
        <div class="container">
            <div class="d-flex align-items-center justify-content-between w-100">
                <span class="navbar-brand">
                    <i class="bi bi-paw" style="color: #58a6ff;"></i> Buscador Semántico de Mascotas
                </span>
                <span class="navbar-text">
                    <i class="bi bi-diagram-3" style="color: #8b949e;"></i> Búsqueda Inteligente
                </span>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    # Navigation with segmented control
    st.markdown("""
    <style>
    .nav-container {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .nav-btn {
        background: #21262d;
        border: 1px solid #30363d;
        color: #8b949e;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
    }
    .nav-btn:hover {
        background: #30363d;
        color: #c9d1d9;
    }
    .nav-btn.active {
        background: #1f6feb;
        border-color: #1f6feb;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    menu = st.segmented_control(
        "Navegación",
        options=["Inicio", "Perros", "Gatos", "Razas", "Dueños"],
        default="Inicio",
        selection_mode="single"
    )

    if menu == "Inicio":
        render_inicio()
    elif menu == "Perros":
        render_perros()
    elif menu == "Gatos":
        render_gatos()
    elif menu == "Razas":
        render_razas()
    elif menu == "Dueños":
        render_duenos()


def render_inicio():
    # Stats
    try:
        todas = get_todas()
        perros = get_perros()
        gatos = get_gatos()
        duenos = get_contar_duenos()

        col_stats = st.columns(4)
        with col_stats[0]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(todas)}</div>
                <div class="stat-label"><i class="bi bi-paw" style="color: #58a6ff;"></i> Total Mascotas</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[1]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(perros)}</div>
                <div class="stat-label"><i class="bi bi-paw" style="color: #f0883e;"></i> Perros</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[2]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(gatos)}</div>
                <div class="stat-label"><i class="bi bi-paw" style="color: #a371f7;"></i> Gatos</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[3]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{duenos}</div>
                <div class="stat-label"><i class="bi bi-people" style="color: #8b949e;"></i> Dueños</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> Error al cargar estadísticas: {e}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### <i class=\"bi bi-search\" style=\"color: #58a6ff;\"></i> Buscar Mascotas", unsafe_allow_html=True)

    # Search
    busqueda = st.text_input(
        "Buscar:",
        placeholder="Busca por nombre, raza, especie, dueño, alimento...",
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
    st.markdown("## <i class=\"bi bi-paw\" style=\"color: #f0883e;\"></i> Perros", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Lista de Perros", "Información Completa"])
    
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
    st.markdown('## <i class="bi bi-paw" style="color: #a371f7;"></i> Gatos', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Lista de Gatos", "Información Completa", "Sin Dueño"])
    
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
    st.markdown('## <i class="bi bi-search" style="color: #58a6ff;"></i> Búsqueda Avanzada', unsafe_allow_html=True)
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
        placeholder="Ej: Bobby, Labrador, Perro, Gato, Carlos, Purina, Collar...",
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
    st.markdown('## <i class="bi bi-collection" style="color: #8b949e;"></i> Razas', unsafe_allow_html=True)
    
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


def render_duenos():
    st.markdown('## <i class="bi bi-people" style="color: #8b949e;"></i> Dueños', unsafe_allow_html=True)

    try:
        from backend.consultas.mascotas import get_mascotas_con_dueno
        resultados = get_mascotas_con_dueno()

        if resultados:
            st.markdown(f"""
            <div class="alert alert-success-custom alert-custom">
                <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} mascotas con dueño
            </div>
            """, unsafe_allow_html=True)
            render_results(resultados, "dueños")
        else:
            st.info("No se encontraron resultados")
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> Error: {e}
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()