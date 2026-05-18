import streamlit as st
from backend.logic import get_todos_los_perros, get_info_completa_perros
from backend.consultas.perros import get_perros_por_raza, get_perros_por_edad
from frontend.components import render_search_input, render_results, render_error, render_warning, render_success


def mostrar_perros():
    st.header("🐕 Perros")
    
    resultados = get_todos_los_perros()
    render_success(f"Se encontraron {len(resultados)} perros")
    if resultados:
        render_results(resultados, "perros")
    else:
        render_warning("No hay perros en la base de datos")


def mostrar_info_perros():
    st.header("📊 Información Completa de Perros")
    
    resultados = get_info_completa_perros()
    render_success(f"Se encontraron {len(resultados)} perros")
    if resultados:
        render_results(resultados, "info_perros")
    else:
        render_warning("No hay perros en la base de datos")


def buscar_perro_por_raza(raza: str):
    return get_perros_por_raza(raza)


def buscar_perro_por_edad(edad: int):
    return get_perros_por_edad(edad)


def main():
    tab1, tab2, tab3 = st.tabs(["🐕 Todos los Perros", "🔍 Buscar por Raza", "📊 Información Completa"])
    
    with tab1:
        mostrar_perros()
    
    with tab2:
        st.subheader("Buscar por Raza")
        raza = st.text_input("Raza:", placeholder="Ej: Labrador, Boxer...")
        if raza:
            resultados = buscar_perro_por_raza(raza)
            if resultados:
                render_success(f"Se encontraron {len(resultados)} perros")
                render_results(resultados, "raza")
            else:
                render_warning(f"No se encontraron perros de raza '{raza}'")
    
    with tab3:
        mostrar_info_perros()


if __name__ == "__main__":
    main()