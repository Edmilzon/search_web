import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.logic import buscar, buscar_avanzado, enriquecer_con_dbpedia, get_todas, get_perros, get_gatos, get_contar_duenos, get_todos_duenos, info_perros, info_gatos

from frontend.components import render_results, clasificar_tipo
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
    st.set_page_config(
        page_title="Buscador de Mascotas",
        page_icon=":dog:",
        layout="wide"
    )

    inject_bootstrap()

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
                    <i class="bi bi-paw" style="color: #58a6ff;"></i> {t("Buscador Semántico de Mascotas", lang)}
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
        "Dueños": t("Dueños", lang),
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
    elif menu == "Dueños":
        render_duenos()


def render_inicio():
    lang = st.session_state.lang
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
                <div class="stat-label"><i class="bi bi-paw" style="color: #58a6ff;"></i> {t("Total Mascotas", lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[1]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(perros)}</div>
                <div class="stat-label"><i class="bi bi-paw" style="color: #f0883e;"></i> {t("Perros", lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[2]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(gatos)}</div>
                <div class="stat-label"><i class="bi bi-paw" style="color: #a371f7;"></i> {t("Gatos", lang)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_stats[3]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{duenos}</div>
                <div class="stat-label"><i class="bi bi-people" style="color: #8b949e;"></i> {t("Dueños", lang)}</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> Error al cargar estadísticas: {e}
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; margin: 2rem 0 1rem 0;">
        <h3><i class="bi bi-search" style="color: #58a6ff;"></i> {t("Búsqueda Inteligente", lang)}</h3>
        <p class="text-muted">{t("Escribe una frase completa para buscar mascotas", lang)}</p>
    </div>
    """, unsafe_allow_html=True)

    busqueda = st.text_input(
        "Buscar:",
        placeholder=t("Buscar por nombre, raza, especie...", lang),
        label_visibility="collapsed",
        key="busqueda_inicio"
    )

    if busqueda:
        try:
            resultados = buscar_avanzado(busqueda)
            if resultados:
                st.markdown(f"""
                <div class="alert alert-success-custom alert-custom">
                    <i class="bi bi-check-circle-fill"></i> {t("Se encontraron", lang)} {len(resultados)} {t("resultado(s)", lang)} "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
                render_results(resultados)

                with st.expander(t("Información desde DBpedia", lang)):
                    st.markdown(f"""
                    <p class="text-muted">
                        <i class="bi bi-database"></i> {t("Datos enriquecidos desde DBpedia (Linked Open Data)", lang)}
                    </p>
                    """, unsafe_allow_html=True)
                    dbpedia_data = enriquecer_con_dbpedia(resultados)
                    if dbpedia_data:
                        for item in dbpedia_data:
                            st.markdown(f"""
                            <div class="card-custom" style="margin-bottom: 1rem;">
                                <h5><i class="bi bi-bookmark"></i> {item.get('raza', '')}</h5>
                                <p><small><a href="{item.get('dbpedia_url', '#')}" target="_blank">{t("Más información aquí", lang)} <i class="bi bi-box-arrow-up-right"></i></a></small></p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info(t("No se encontraron datos adicionales en DBpedia para estas razas.", lang))
            else:
                st.markdown(f"""
                <div class="alert alert-warning-custom alert-custom">
                    <i class="bi bi-exclamation-circle-fill"></i> {t("No se encontraron resultados", lang)} "{busqueda}"
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="alert alert-danger-custom alert-custom">
                <i class="bi bi-exclamation-triangle-fill"></i> {t("Error", lang)}: {e}
            </div>
            """, unsafe_allow_html=True)


def render_duenos():
    import pandas as pd
    lang = st.session_state.lang
    st.markdown(f'## <i class="bi bi-people" style="color: #8b949e;"></i> {t("Dueños", lang)}', unsafe_allow_html=True)

    try:
        duenos_data = get_todos_duenos()
        df = pd.DataFrame(duenos_data)

        st.markdown(f"""
        <div class="alert alert-success-custom alert-custom">
            <i class="bi bi-check-circle-fill"></i> {t("Se encontraron", lang)} {df['Due\u00f1o'].nunique()} {t("Dueños", lang).lower()}
        </div>
        """, unsafe_allow_html=True)

        if 'Dueño' in df.columns:
            for dueño, grupo in df.groupby('Dueño'):
                with st.expander(f"👤 {dueño} ({len(grupo)} {t('Mascotas', lang).lower()})"):
                    grupo['Tipo'] = grupo['Raza'].apply(clasificar_tipo)
                    st.dataframe(
                        grupo[['Nombre', 'Raza', 'Tipo']].reset_index(drop=True),
                        column_config={
                            "Tipo": st.column_config.TextColumn(t("Tipo", lang), width="small")
                        },
                        width="stretch",
                        hide_index=True
                    )
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> {t("Error", lang)}: {e}
        </div>
        """, unsafe_allow_html=True)


def _render_especie_detallada(titulo: str, color: str, info_fn, lang: str):
    import pandas as pd
    st.markdown(f'## <i class="bi bi-paw" style="color: {color};"></i> {titulo}', unsafe_allow_html=True)
    try:
        resultados = info_fn()
        df = pd.DataFrame(resultados)
        razas = df['Raza'].nunique() if 'Raza' in df.columns else 0
        st.markdown(f"""
        <div class="alert alert-success-custom alert-custom">
            <i class="bi bi-check-circle-fill"></i> {t("Se encontraron", lang)} {len(df)} {t("resultado(s)", lang)} ({razas} {t("Razas", lang).lower()})
        </div>
        """, unsafe_allow_html=True)
        if not resultados:
            return
        df['Tipo'] = df['Raza'].apply(clasificar_tipo)
        cols = [c for c in ['Nombre', 'Edad', 'Peso', 'Color', 'Raza', 'Tipo', 'Due\u00f1o', 'Alimento'] if c in df.columns]
        for raza, grupo in df.groupby('Raza'):
            with st.expander(f"🐾 {raza} ({len(grupo)} {t('Mascotas', lang).lower()})"):
                st.dataframe(
                    grupo[cols].reset_index(drop=True),
                    column_config={
                        "Tipo": st.column_config.TextColumn(t("Tipo", lang), width="small")
                    },
                    width="stretch",
                    hide_index=True
                )
    except Exception as e:
        st.markdown(f"""
        <div class="alert alert-danger-custom alert-custom">
            <i class="bi bi-exclamation-triangle-fill"></i> {t("Error", lang)}: {e}
        </div>
        """, unsafe_allow_html=True)


def render_perros():
    _render_especie_detallada(t("Perros", st.session_state.lang), "#f0883e", info_perros, st.session_state.lang)


def render_gatos():
    _render_especie_detallada(t("Gatos", st.session_state.lang), "#a371f7", info_gatos, st.session_state.lang)


if __name__ == "__main__":
    main()
