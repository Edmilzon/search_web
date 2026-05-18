from .base import ejecutar_query, cargar_ontologia


def get_todas_las_mascotas():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def buscar_por_nombre_mascota(termino: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      FILTER(CONTAINS(LCASE(?nombreMascota), LCASE("{termino}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def buscar_por_raza(termino: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      FILTER(CONTAINS(LCASE(?nombreRaza), LCASE("{termino}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def get_mascotas_con_dueno():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?mascota) (STR(?nombreDueño) AS ?dueño)
    WHERE {
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneDueño ?dueño .
      ?dueño :nombreDueño ?nombreDueño .
    }
    """
    return _mapear_resultados(query, ["Mascota", "Dueño"])


def get_mascotas_sin_dueno():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT ?mascota (STR(?nombreMascota) AS ?nombre)
    WHERE {
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      FILTER NOT EXISTS { ?mascota :tieneDueño ?dueño }
    }
    """
    return _mapear_resultados(query, ["Nombre"])


def get_mascotas_por_edad(edad: int):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?edadMascota) AS ?edad)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      FILTER(?edadMascota = {edad})
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Edad"])


def get_mascotas_por_peso(peso: float):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?pesoMascota) AS ?peso)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :pesoMascota ?pesoMascota .
      FILTER(?pesoMascota = {peso})
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Peso"])


def get_mascotas_sin_bozal():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre)
    WHERE {
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :requiereBozal false .
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre"])


def get_mascotas_por_cuidado(tipo_cuidado: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?cuidado) AS ?tipo_cuidado)
    WHERE {{
      ?m rdf:type :Mascota .
      ?m :nombreMascota ?nombreMascota .
      ?m :perteneceAEspecie ?especie .
      ?especie :nombreEspecie ?nE .
      FILTER(CONTAINS(LCASE(?nE), LCASE("{tipo_cuidado}")))
      ?m :requiereCuidado ?c .
      ?c :tipoCuidado ?tipo .
      BIND(STR(?tipo) AS ?cuidado)
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Tipo de Cuidado"])


def get_mascotas_por_alimento(marca: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?marca) AS ?alimento)
    WHERE {{
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :consume ?alimento .
      ?alimento :marcaAlimento ?marca .
      FILTER(CONTAINS(LCASE(?marca), LCASE("{marca}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Alimento"])


def get_mascotas_por_tipo_alimento(tipo: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?tipo) AS ?tipo_alimento)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :consume ?alimento .
      ?alimento :tipoAlimento ?tipo .
      FILTER(CONTAINS(LCASE(?tipo), LCASE("{tipo}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Tipo de Alimento"])


def get_mascotas_por_accesorio(accesorio: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreAccesorio) AS ?accesorio)
    WHERE {{
      ?mascota :usa ?accesorioObj .
      ?mascota :nombreMascota ?nombreMascota .
      ?accesorioObj :nombreAccesorio ?nombreAccesorio .
      FILTER(CONTAINS(LCASE(?nombreAccesorio), LCASE("{accesorio}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Accesorio"])


def get_mascotas_por_pelaje(tipo_pelaje: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?pelaje) AS ?tipo_pelaje)
    WHERE {{
      ?mascota :tipoPelaje ?pelaje .
      ?mascota :nombreMascota ?nombreMascota .
      FILTER(CONTAINS(LCASE(?pelaje), LCASE("{tipo_pelaje}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Tipo de Pelaje"])


def get_mascotas_por_especie_y_edad(especie: str, edad: int):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?edadMascota) AS ?edad) (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      ?raza :perteneceAEspecie ?especie .
      ?especie :nombreEspecie ?nombreEspecie .
      FILTER(?edadMascota = {edad} && ?nombreEspecie = "{especie}")
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Edad", "Raza"])


def get_info_completa_mascota(nombre: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT DISTINCT 
           (STR(?nombreMascota) AS ?nombre) 
           (STR(?edadMascota) AS ?edad)
           (STR(?pesoMascota) AS ?peso)
           (STR(?colorMascota) AS ?color)
           (STR(?sexoMascota) AS ?sexo)
           (STR(?nombreRaza) AS ?raza)
           (STR(?nombreEspecie) AS ?especie)
           (STR(?nombreDueño) AS ?dueño)
           (STR(?marcaAlimento) AS ?alimento)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      OPTIONAL {{ ?mascota :edadMascota ?edadMascota . }}
      OPTIONAL {{ ?mascota :pesoMascota ?pesoMascota . }}
      OPTIONAL {{ ?mascota :colorMascota ?colorMascota . }}
      OPTIONAL {{ ?mascota :sexoMascota ?sexoMascota . }}
      OPTIONAL {{
        ?mascota :tieneRaza ?raza .
        ?raza :nombreRaza ?nombreRaza .
        OPTIONAL {{ ?raza :perteneceAEspecie ?especieObj . ?especieObj :nombreEspecie ?nombreEspecie . }}
      }}
      OPTIONAL {{ ?mascota :tieneDueño ?dueñoObj . ?dueñoObj :nombreDueño ?nombreDueño . }}
      OPTIONAL {{ ?mascota :consume ?alimentoObj . ?alimentoObj :marcaAlimento ?marcaAlimento . }}
      FILTER(CONTAINS(LCASE(?nombreMascota), LCASE("{nombre}")))
    }}
    """
    return _mapear_resultados(query, ["Nombre", "Edad", "Peso", "Color", "Sexo", "Raza", "Especie", "Dueño", "Alimento"])


def get_todas_las_raza():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreRaza) AS ?raza) (STR(?nombreEspecie) AS ?especie)
    WHERE {
      ?razaInd :perteneceAEspecie ?especieInd .
      ?razaInd :nombreRaza ?nombreRaza .
      ?especieInd :nombreEspecie ?nombreEspecie .
    }
    ORDER BY ?especie ?raza
    """
    return _mapear_resultados(query, ["Raza", "Especie"])


def get_razas_con_mas_de_una_mascota():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreRaza) AS ?raza) 
           (GROUP_CONCAT(STR(?nombreMascota); SEPARATOR=", ") AS ?mascotas)
    WHERE {
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      ?mascota :nombreMascota ?nombreMascota .
    }
    GROUP BY ?raza ?nombreRaza
    HAVING (COUNT(?mascota) > 1)
    ORDER BY ?raza
    """
    return _mapear_resultados(query, ["Raza", "Mascotas"])


def _mapear_resultados(query: str, columnas: list) -> list:
    resultados = ejecutar_query(query)
    datos = []
    for fila in resultados:
        datos.append(resultado_to_dict(fila, columnas))
    return datos


def resultado_to_dict(fila, columnas: list) -> dict:
    return {col: str(fila[i]) if hasattr(fila[i], '__str__') else str(fila[i]) for i, col in enumerate(columnas)}