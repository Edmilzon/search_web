from .base import ejecutar_query


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


def get_gatos_por_raza(raza: str):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :perteneceAEspecie ?especie .
      ?mascota :nombreMascota ?nombreMascota .
      ?razaObj :nombreRaza ?nombreRaza .
      ?especie :nombreEspecie "Gato"^^xsd:string .
      FILTER(CONTAINS(LCASE(?nombreRaza), LCASE("{raza}")))
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Raza"])


def get_gatos_por_edad(edad: int):
    query = f"""
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?edadMascota) AS ?edad) (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      ?raza :perteneceAEspecie ?especie .
      ?especie :nombreEspecie "Gato"^^xsd:string .
      FILTER(?edadMascota = {edad})
    }}
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Edad", "Raza"])


def get_gatos_por_alimento():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?marca) AS ?alimento)
    WHERE {
      ?m a :Mascota .
      ?m :nombreMascota ?nombreMascota .
      OPTIONAL { ?m :tieneRaza ?r . }
      OPTIONAL { ?r :perteneceAEspecie ?e . }
      OPTIONAL { ?e :nombreEspecie ?esp . }
      OPTIONAL { ?m :consume ?a . }
      OPTIONAL { ?a :marcaAlimento ?marca . }
      FILTER(?esp = "Gato")
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Alimento"])


def get_gatos_por_cuidado():
    query = """
    PREFIX : <http://www.semanticweb.org/mascotas#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?cuidado) AS ?tipo_cuidado)
    WHERE {
      ?m rdf:type :Mascota .
      ?m :nombreMascota ?nom .
      ?m :perteneceAEspecie ?especie . 
      ?especie :nombreEspecie ?nE .
      FILTER(STR(?nE) = "Gato") 
      ?m :requiereCuidado ?c .
      ?c :tipoCuidado ?tipo .
      BIND(STR(?nom) AS ?nombreMascota)
      BIND(STR(?tipo) AS ?cuidado)
    }
    ORDER BY ?nombre
    """
    return _mapear_resultados(query, ["Nombre", "Tipo de Cuidado"])


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


def _mapear_resultados(query: str, columnas: list) -> list:
    resultados = ejecutar_query(query)
    datos = []
    for fila in resultados:
        fila_dict = {}
        for i, col in enumerate(columnas):
            try:
                fila_dict[col] = str(fila[i]) if fila[i] else ""
            except:
                fila_dict[col] = ""
        datos.append(fila_dict)
    return datos