from rdflib import Graph
import os

_ONTOLOGY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "..",
    "database",
    "mascotas.rdf"
)

_grafo_cache = None


def cargar_ontologia():
    global _grafo_cache
    if _grafo_cache is None:
        _grafo_cache = Graph()
        _grafo_cache.parse(_ONTOLOGY_PATH, format="xml")
    return _grafo_cache


def ejecutar_query(query: str) -> list:
    grafo = cargar_ontologia()
    try:
        resultados = grafo.query(query)
        return list(resultados)
    except Exception as e:
        print(f"Error en query: {e}")
        return []