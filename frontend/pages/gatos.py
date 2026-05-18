import streamlit as st
from backend.logic import get_todos_los_gatos, get_info_completa_gatos
from backend.consultas.gatos import get_gatos_por_raza, get_gatos_por_edad, get_gatos_sin_dueno
from frontend.components import render_search_input, render_results, render_error, render_warning, render_success


def mostrar_gatos():
    st.header("🐈 Gatos")
    
    resultados = get_todos_los_gatos()
    render_success(f"Se encontraron {len(resultados)} gatos")
    if resultados:
        render_results(resultados, "gatos")
    else:
        render_warning("No hay gatos en la base de datos")


def mostrar_info_gatos():
    st.header("📊 Información Completa de Gatos")
    
    resultados = get_info_completa_gatos()
    render_success(f"Se encontraron {len(resultados)} gatos")
    if resultados:
        render_results(resultados, "info_gatos")
    else:
        render_warning("No hay gatos en la base de datos")


def mostrar_gatos_sin_dueño():
    st.header("🐈 Gatos sin Dueño")
    
    resultados = get_gatos_sin_dueno()
    render_success(f"Se encontraron {len(resultados)} gatos sin dueño")
    if resultados:
        render_results(resultados, "sin_dueño")
    else:
        render_warning("No hay gatos sin dueño en la base de datos")


def buscar_gato_por_raza(raza: str):
    return get_gatos_por_raza(raza)


def buscar_gato_por_edad(edad: int):
    return get_gatos_por_edad(edad)


def main():
    tab1, tab2, tab3, tab4 = st.tabs(["🐈 Todos los Gatos", "🔍 Buscar por Raza", "🐈 Sin Dueño", "📊 Información Completa"])
    
    with tab1:
        mostrar_gatos()
    
    with tab2:
        st.subheader("Buscar por Raza")
        raza = st.text_input("Raza:", placeholder="Ej: Siamés, Persa...")
        if raza:
            resultados = buscar_gato_por_raza(raza)
            if resultados:
                render_success(f"Se encontraron {len(resultados)} gatos")
                render_results(resultados, "raza")
            else:
                render_warning(f"No se encontraron gatos de raza '{raza}'")
    
    with tab3:
        mostrar_gatos_sin_dueño()
    
    with tab4:
        mostrar_info_gatos()


if __name__ == "__main__":
    main()