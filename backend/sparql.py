from rdflib import Graph
import os
from owlrl import DeductiveClosure, OWLRL_Semantics

_ONTOLOGY_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "database",
    "mascotas.rdf"
)

_grafo_cache = None


def cargar_ontologia(aplicar_razonamiento=True):
    global _grafo_cache
    if _grafo_cache is None:
        _grafo_cache = Graph()
        _grafo_cache.parse(_ONTOLOGY_PATH, format="xml")
        if aplicar_razonamiento:
            DeductiveClosure(OWLRL_Semantics).expand(_grafo_cache)
    return _grafo_cache


def ejecutar_query(query: str) -> list:
    grafo = cargar_ontologia()
    try:
        resultados = grafo.query(query)
        return list(resultados)
    except Exception as e:
        print(f"Error en query: {e}")
        return []


def _mapear_resultados(query: str, columnas: list) -> list:
    resultados = ejecutar_query(query)
    datos = []
    for fila in resultados:
        fila_dict = {}
        for i, col in enumerate(columnas):
            try:
                fila_dict[col] = str(fila[i]) if fila[i] else ""
            except Exception:
                fila_dict[col] = ""
        datos.append(fila_dict)
    return datos


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
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreDueño) AS ?dueño)
           (STR(?nombreRaza) AS ?raza)
    WHERE {
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneDueño ?dueño .
      ?dueño :nombreDueño ?nombreDueño .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
    }
    """
    return _mapear_resultados(query, ["Nombre", "Dueño", "Raza"])


def get_mascotas_sin_dueno():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      FILTER NOT EXISTS { ?mascota :tieneDueño ?dueño }
    }
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def get_mascotas_por_edad(edad: int):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?edadMascota) AS ?edad)
           (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      FILTER(?edadMascota = {edad})
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Edad", "Raza"])


def get_mascotas_por_alimento(marca: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?marca) AS ?alimento)
           (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :consume ?alimento .
      ?alimento :marcaAlimento ?marca .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      FILTER(CONTAINS(LCASE(?marca), LCASE("{marca}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Alimento", "Raza"])


def get_mascotas_por_accesorio(accesorio: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreAccesorio) AS ?accesorio)
           (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :usa ?accesorioObj .
      ?mascota :nombreMascota ?nombreMascota .
      ?accesorioObj :nombreAccesorio ?nombreAccesorio .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      FILTER(CONTAINS(LCASE(?nombreAccesorio), LCASE("{accesorio}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Accesorio", "Raza"])


def get_mascotas_por_pelaje(tipo_pelaje: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?pelaje) AS ?tipo_pelaje)
           (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :tipoPelaje ?pelaje .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      FILTER(CONTAINS(LCASE(?pelaje), LCASE("{tipo_pelaje}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Tipo de Pelaje", "Raza"])


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


def get_todos_los_perros():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {
      ?mascota :tieneRaza ?raza .
      ?raza :perteneceAEspecie :Especie2 .
      ?mascota :nombreMascota ?nombreMascota .
      ?raza :nombreRaza ?nombreRaza .
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def get_info_completa_perros():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) 
           (STR(?edadMascota) AS ?edad)
           (STR(?pesoMascota) AS ?peso)
           (STR(?colorMascota) AS ?color)
           (STR(?nombreRaza) AS ?raza)
           (STR(?nombreDueño) AS ?dueño)
           (STR(?marcaAlimento) AS ?alimento)
    WHERE {
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      ?mascota :pesoMascota ?pesoMascota .
      ?mascota :colorMascota ?colorMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      ?raza :perteneceAEspecie ?especie .
      ?especie :nombreEspecie "Perro"^^xsd:string .
      OPTIONAL { ?mascota :tieneDueño ?dueñoObj . ?dueñoObj :nombreDueño ?nombreDueño . }
      OPTIONAL { ?mascota :consume ?alimentoObj . ?alimentoObj :marcaAlimento ?marcaAlimento . }
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Edad", "Peso", "Color", "Raza", "Dueño", "Alimento"])


def get_todos_los_gatos():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {
      ?mascota :tieneRaza ?raza .
      ?raza :perteneceAEspecie :Especie1 .
      ?mascota :nombreMascota ?nombreMascota .
      ?raza :nombreRaza ?nombreRaza .
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def get_info_completa_gatos():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) 
           (STR(?edadMascota) AS ?edad)
           (STR(?pesoMascota) AS ?peso)
           (STR(?colorMascota) AS ?color)
           (STR(?nombreRaza) AS ?raza)
           (STR(?nombreDueño) AS ?dueño)
           (STR(?marcaAlimento) AS ?alimento)
    WHERE {
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      ?mascota :pesoMascota ?pesoMascota .
      ?mascota :colorMascota ?colorMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      ?raza :perteneceAEspecie ?especie .
      ?especie :nombreEspecie "Gato"^^xsd:string .
      OPTIONAL { ?mascota :tieneDueño ?dueñoObj . ?dueñoObj :nombreDueño ?nombreDueño . }
      OPTIONAL { ?mascota :consume ?alimentoObj . ?alimentoObj :marcaAlimento ?marcaAlimento . }
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Edad", "Peso", "Color", "Raza", "Dueño", "Alimento"])


def get_gatos_sin_dueno():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre)
    WHERE {
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :perteneceAEspecie ?especie .
      ?especie :nombreEspecie "Gato"^^xsd:string .
      FILTER NOT EXISTS { ?mascota :tieneDueño ?dueño }
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre"])
