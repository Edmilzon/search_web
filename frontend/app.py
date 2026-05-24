import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.logic import buscar, buscar_avanzado, enriquecer_con_dbpedia, get_todas, get_perros, get_gatos, get_razas, get_contar_duenos

from frontend.components import render_results, render_results_raza
from backend.i18n import t


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

    if "lang" not in st.session_state:
        st.session_state.lang = "es"

    col_lang, _ = st.columns([1, 11])
    with col_lang:
        lang = st.selectbox(
            "Language",
            options=["es", "en"],
            format_func=lambda x: "🇪🇸 Español" if x == "es" else "🇬🇧 English",
            key="lang",
            label_visibility="collapsed"
        )

    st.markdown(f"""
    <nav class="navbar-custom">
        <div class="container">
            <div class="d-flex align-items-center justify-content-between w-100">
                <span class="navbar-brand">
                    <i class="bi bi-paw" style="color: #58a6ff;"></i> Buscador Semántico de Mascotas
                </span>
                <span class="navbar-text">
                    <i class="bi bi-diagram-3" style="color: #8b949e;"></i> {t("Búsqueda Inteligente", lang)}
                </span>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    opciones_menu = {
        "Inicio": t("Inicio", lang),
        "Perros": t("Perros", lang),
        "Gatos": t("Gatos", lang),
        "Razas": t("Razas", lang),
    }
    menu = st.segmented_control(
        "Navigation",
        options=list(opciones_menu.keys()),
        format_func=lambda x: opciones_menu[x],
        default="Inicio",
        selection_mode="single",
        label_visibility="collapsed"
    )

    if menu == "Inicio":
        render_inicio()
    elif menu == "Perros":
        render_perros()
    elif menu == "Gatos":
        render_gatos()
    elif menu == "Razas":
        render_razas()


def render_inicio():
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

    st.markdown("""
    <div style="text-align:center; margin: 2rem 0 1rem 0;">
        <h3><i class="bi bi-search" style="color: #58a6ff;"></i> Búsqueda Inteligente</h3>
        <p class="text-muted">Escribe una frase completa para buscar mascotas</p>
    </div>
    """, unsafe_allow_html=True)

    busqueda = st.text_input(
        "Buscar:",
        placeholder="",
        label_visibility="collapsed",
        key="busqueda_inicio"
    )

    if busqueda:
        try:
            resultados = buscar_avanzado(busqueda)
            if resultados:
                st.markdown(f"""
                <div class="alert alert-success-custom alert-custom">
                    <i class="bi bi-check-circle-fill"></i> Se encontraron {len(resultados)} resultado(s) para "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
                render_results(resultados, busqueda)

                with st.expander("Información desde DBpedia"):
                    st.markdown("""
                    <p class="text-muted">
                        <i class="bi bi-database"></i> Datos enriquecidos desde DBpedia (Linked Open Data)
                    </p>
                    """, unsafe_allow_html=True)
                    dbpedia_data = enriquecer_con_dbpedia(resultados)
                    if dbpedia_data:
                        for item in dbpedia_data:
                            st.markdown(f"""
                            <div class="card-custom" style="margin-bottom: 1rem;">
                                <h5><i class="bi bi-bookmark"></i> {item.get('raza', '')}</h5>
                                <p><strong>Origen:</strong> {item.get('origin', 'No disponible')}</p>
                                <p><strong>Peso promedio:</strong> {item.get('weight', 'No disponible')}</p>
                                <p><strong>Esperanza de vida:</strong> {item.get('lifeSpan', 'No disponible')}</p>
                                <p><small><a href="{item.get('dbpedia_url', '#')}" target="_blank">Ver en DBpedia <i class="bi bi-box-arrow-up-right"></i></a></small></p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No se encontraron datos adicionales en DBpedia para estas razas.")
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


def render_gatos():
    st.markdown('## <i class="bi bi-paw" style="color: #a371f7;"></i> Gatos', unsafe_allow_html=True)

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


if __name__ == "__main__":
    main()
