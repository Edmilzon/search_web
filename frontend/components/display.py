import streamlit as st
import pandas as pd


_PERRO_BREEDS = ['labrador', 'bulldog', 'pastor', 'golden', 'poodle', 'chihuahua', 'beagle', 'rottweiler', 'yorkshire', 'boxer', 'doberman', 'husky', 'shih tzu', 'border', 'collie', 'akita']
_GATO_BREEDS = ['persa', 'siamés', 'maine', 'bengala', 'ragdoll', 'british', 'esfinge', 'azul', 'abisinio', 'scottish', 'angora', 'savannah', 'bombay', 'noruego', 'birmano']


def clasificar_tipo(raza: str) -> str:
    raza_lower = raza.lower()
    if any(p in raza_lower for p in _PERRO_BREEDS):
        return "🐕 Perro"
    if any(g in raza_lower for g in _GATO_BREEDS):
        return "🐈 Gato"
    return ""


def render_results(resultados):

    if not resultados:
        st.info("No se encontraron resultados")
        return

    df = pd.DataFrame(resultados)

    if 'Raza' in df.columns:
        df['Tipo'] = df['Raza'].apply(clasificar_tipo)

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "Tipo": st.column_config.TextColumn("Tipo", width="small")
        }
    )


def render_error(mensaje: str):
    st.markdown(f"""
    <div class="alert alert-danger alert-custom" role="alert">
        <i class="bi bi-exclamation-triangle-fill"></i> {mensaje}
    </div>
    """, unsafe_allow_html=True)


def render_warning(mensaje: str):
    st.markdown(f"""
    <div class="alert alert-warning alert-custom" role="alert">
        <i class="bi bi-exclamation-circle-fill"></i> {mensaje}
    </div>
    """, unsafe_allow_html=True)


def render_success(mensaje: str):
    st.markdown(f"""
    <div class="alert alert-success alert-custom" role="alert">
        <i class="bi bi-check-circle-fill"></i> {mensaje}
    </div>
    """, unsafe_allow_html=True)

