import streamlit as st
from backend.logic import buscar
from frontend.components import render_search_input, render_results, render_error, render_warning, render_success


def main():
    st.header("🔍 Búsqueda Avanzada")
    st.markdown("""
    **Buscar por:** nombre, raza, especie (perro/gato), nombre del dueño, 
    marca de alimento, accesorio, tipo de pelaje
    """)
    
    busqueda = render_search_input(
        placeholder="Ej: Bobby, Labrador, Perro, Gato, Carlos, Purina, Collar..."
    )
    
    if busqueda:
        try:
            resultados = buscar(busqueda)
            if resultados:
                render_success(f"Se encontraron {len(resultados)} resultado(s)")
                render_results(resultados, busqueda)
            else:
                render_warning(f"No se encontraron resultados para '{busqueda}'")
        except Exception as e:
            render_error(f"Error: {e}")
    else:
        render_warning("Escribe un término de búsqueda")


if __name__ == "__main__":
    main()