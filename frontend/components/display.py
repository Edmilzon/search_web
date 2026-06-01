import streamlit as st
import pandas as pd

from backend.sparql import t


_PERRO_BREEDS = ['labrador', 'bulldog', 'pastor', 'golden', 'poodle', 'chihuahua', 'beagle', 'rottweiler', 'yorkshire', 'boxer', 'doberman', 'husky', 'shih tzu', 'border', 'collie', 'akita']
_GATO_BREEDS = ['persa', 'siamés', 'maine', 'bengala', 'ragdoll', 'british', 'esfinge', 'azul', 'abisinio', 'scottish', 'angora', 'savannah', 'bombay', 'noruego', 'birmano']


def clasificar_tipo(raza: str) -> str:
    raza_lower = raza.lower()
    if any(p in raza_lower for p in _PERRO_BREEDS):
        return "🐕 Perro"
    if any(g in raza_lower for g in _GATO_BREEDS):
        return "🐈 Gato"
    return ""


_COL_ORDER = ["Nombre", "Edad", "Peso", "Color", "Sexo", "Raza", "Especie", "Tipo",
              "Dueño", "Alimento", "Accesorio", "Tipo de Pelaje", "Temperamento",
              "Cuidado", "Frecuencia", "Tipo de Alimento"]


def render_results(resultados, lang="es"):

    if not resultados:
        st.info(t("No se encontraron resultados", lang))
        return

    df = pd.DataFrame(resultados)

    if 'Raza' in df.columns:
        df['Tipo'] = df['Raza'].apply(clasificar_tipo)

    ordered = [c for c in _COL_ORDER if c in df.columns]
    remaining = [c for c in df.columns if c not in _COL_ORDER]
    df = df[ordered + remaining]

    column_config = {}
    for col in df.columns:
        column_config[col] = st.column_config.TextColumn(t(col, lang))

    st.dataframe(
        df,
        column_config=column_config,
        width="stretch",
        hide_index=True,
    )

