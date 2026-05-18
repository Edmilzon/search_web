import streamlit as st
from backend.logic import get_todas, get_todas_las_raza
from frontend.components import render_search_input, render_results, render_results_raza, render_error, render_warning, render_success


def mostrar_mascotas():
    st.header("🐾 Todas las Mascotas")
    
    resultados = get_todas()
    render_success(f"Se encontraron {len(resultados)} mascotas")
    if resultados:
        render_results(resultados, "todas")
    else:
        render_warning("No hay mascotas en la base de datos")


def mostrar_raza():
    st.header("🐶 Razas")
    
    resultados = get_todas_las_raza()
    render_success(f"Se encontraron {len(resultados)} razas")
    if resultados:
        render_results_raza(resultados)
    else:
        render_warning("No hay razas en la base de datos")


def main():
    tab1, tab2 = st.tabs(["🐾 Mascotas", "🐶 Razas"])
    
    with tab1:
        mostrar_mascotas()
    
    with tab2:
        mostrar_raza()


if __name__ == "__main__":
    main()