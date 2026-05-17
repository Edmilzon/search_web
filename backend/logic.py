from rdflib import Graph
import os

_ONTOLOGY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mascotas.owl")

def cargar_ontologia():
    g = Graph()
    g.parse(_ONTOLOGY_PATH, format="xml")
    return g

def buscar_por_especie(especie: str):
    grafo = cargar_ontologia()
    
    query_sparql = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?nombresMascota ?nombresRaza
    WHERE {{
      ?mascota :tieneRaza ?raza .
      ?raza :perteneceAEspecie ?especie .

      ?mascota :nombre ?nombresMascota .
      ?raza :nombre ?nombresRaza .
      
      ?especie :nombre "{especie}"^^xsd:string .
    }}
    """
    
    resultados = grafo.query(query_sparql)
    
    datos = []
    for fila in resultados:
        datos.append({
            "Nombre de la Mascota": str(fila.nombresMascota),
            "Raza": str(fila.nombresRaza)
        })
    
    return datos