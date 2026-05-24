from rdflib import Graph
import os
import re
from owlrl import DeductiveClosure, OWLRL_Semantics


def _sanitizar(valor):
    return re.sub(r'["\\]', '', str(valor))

_ONTOLOGY_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "database",
    "mascotas.rdf"
)

_grafo_cache = None

_PREF = "PREFIX : <http://www.semanticweb.org/mascotas#>"


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


def _q(select: str, where: str, columnas: list, orden: str = "") -> list:
    q = f"{_PREF} SELECT {select} WHERE {{{where}}}"
    if orden:
        q += f" ORDER BY {orden}"
    return _mapear_resultados(q, columnas)


def _base_mascota(select_extras: str = "", triples_extra: str = "",
                  filtro: str = "", orden: str = "?nombre") -> str:
    return f"""
    {_PREF}
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
           {select_extras}
    WHERE {{
      ?mascota a :Mascota .
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      {triples_extra}
      {filtro}
    }}
    ORDER BY {orden}
    """


def _salida(columnas: list, query: str) -> list:
    return _mapear_resultados(query, columnas)


def get_todas_las_mascotas():
    return _salida(["Nombre", "Raza"],
                   _base_mascota())


def buscar_por_nombre_mascota(termino: str):
    return _salida(["Nombre", "Raza"],
                   _base_mascota(
                       filtro=f'FILTER(CONTAINS(LCASE(?nombreMascota), LCASE("{_sanitizar(termino)}")))'
                   ))


def buscar_por_raza(termino: str):
    return _salida(["Nombre", "Raza"],
                   _base_mascota(
                       filtro=f'FILTER(CONTAINS(LCASE(?nombreRaza), LCASE("{_sanitizar(termino)}")))'
                   ))


def get_mascotas_con_dueno():
    return _salida(["Nombre", "Due\u00f1o", "Raza"],
                   f"""
    {_PREF}
    SELECT (STR(?nombreMascota) AS ?nombre) (STR(?nombreDue\u00f1o) AS ?due\u00f1o)
           (STR(?nombreRaza) AS ?raza)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneDue\u00f1o ?due\u00f1o .
      ?due\u00f1o :nombreDue\u00f1o ?nombreDue\u00f1o .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
    }}
    """)


def get_mascotas_sin_dueno():
    return _salida(["Nombre", "Raza"],
                   _base_mascota(
                       filtro="FILTER NOT EXISTS { ?mascota :tieneDue\u00f1o ?due\u00f1o }"
                   ))


def get_mascotas_por_edad(edad: int):
    return _salida(["Nombre", "Raza", "Edad"],
                   _base_mascota(
                       select_extras="(STR(?edadMascota) AS ?edad)",
                       triples_extra="?mascota :edadMascota ?edadMascota .",
                       filtro=f"FILTER(?edadMascota = {edad})"
                   ))


def get_mascotas_por_alimento(marca: str):
    return _salida(["Nombre", "Raza", "Alimento"],
                   _base_mascota(
                       select_extras='(STR(?marcaAli) AS ?alimento)',
                       triples_extra="?mascota :consume ?alimento . ?alimento :marcaAlimento ?marcaAli .",
                       filtro=f'FILTER(CONTAINS(LCASE(?marcaAli), LCASE("{_sanitizar(marca)}")))'
                   ))


def get_mascotas_por_accesorio(accesorio: str):
    return _salida(["Nombre", "Raza", "Accesorio"],
                   _base_mascota(
                       select_extras="(STR(?nombreAccesorio) AS ?accesorio)",
                       triples_extra="?mascota :usa ?accesorioObj . ?accesorioObj :nombreAccesorio ?nombreAccesorio .",
                       filtro=f'FILTER(CONTAINS(LCASE(?nombreAccesorio), LCASE("{_sanitizar(accesorio)}")))'
                   ))


def get_mascotas_por_pelaje(tipo_pelaje: str):
    return _salida(["Nombre", "Raza", "Tipo de Pelaje"],
                   _base_mascota(
                       select_extras="(STR(?pelaje) AS ?tipo_pelaje)",
                       triples_extra="?mascota :tipoPelaje ?pelaje .",
                       filtro=f'FILTER(CONTAINS(LCASE(?pelaje), LCASE("{_sanitizar(tipo_pelaje)}")))'
                   ))


def get_mascotas_por_color(color: str):
    return _salida(["Nombre", "Raza", "Color"],
                   _base_mascota(
                       select_extras="(STR(?colorMascota) AS ?color)",
                       triples_extra="?mascota :colorMascota ?colorMascota .",
                       filtro=f'FILTER(CONTAINS(LCASE(?colorMascota), LCASE("{_sanitizar(color)}")))'
                   ))


def get_mascotas_por_sexo(sexo: str):
    return _salida(["Nombre", "Raza", "Sexo"],
                   _base_mascota(
                       select_extras="(STR(?sexoMascota) AS ?sexo)",
                       triples_extra="?mascota :sexoMascota ?sexoMascota .",
                       filtro=f'FILTER(CONTAINS(LCASE(?sexoMascota), LCASE("{_sanitizar(sexo)}")))'
                   ))


def get_mascotas_por_esterilizado(esterilizado: bool):
    val = "true" if esterilizado else "false"
    return _salida(["Nombre", "Raza"],
                   _base_mascota(
                       triples_extra="?mascota :esterilizado ?esterilizado .",
                       filtro=f"FILTER(?esterilizado = {val})"
                   ))


def get_mascotas_por_requiere_bozal(requiere: bool):
    val = "true" if requiere else "false"
    return _salida(["Nombre", "Raza"],
                   _base_mascota(
                       triples_extra="?mascota :requiereBozal ?requiereBozal .",
                       filtro=f"FILTER(?requiereBozal = {val})"
                   ))


def get_mascotas_por_temperamento(temperamento: str):
    return _salida(["Nombre", "Raza", "Temperamento"],
                   _base_mascota(
                       select_extras="(STR(?temperamento) AS ?temperamento)",
                       triples_extra="?razaObj :temperamento ?temperamento .",
                       filtro=f'FILTER(CONTAINS(LCASE(?temperamento), LCASE("{_sanitizar(temperamento)}")))'
                   ))


def get_mascotas_por_tipo_alimento(tipo: str):
    return _salida(["Nombre", "Raza", "Tipo de Alimento"],
                   _base_mascota(
                       select_extras="(STR(?tipoAlimento) AS ?tipo_alimento)",
                       triples_extra="?mascota :consume ?alimento . ?alimento :tipoAlimento ?tipoAlimento .",
                       filtro=f'FILTER(CONTAINS(LCASE(?tipoAlimento), LCASE("{_sanitizar(tipo)}")))'
                   ))


def get_mascotas_por_cuidado(tipo_cuidado: str):
    return _salida(["Nombre", "Raza", "Cuidado"],
                   _base_mascota(
                       select_extras="(STR(?tipoCuidado) AS ?cuidado)",
                       triples_extra="?mascota :requiereCuidado ?cuidadoObj . ?cuidadoObj :tipoCuidado ?tipoCuidado .",
                       filtro=f'FILTER(CONTAINS(LCASE(?tipoCuidado), LCASE("{_sanitizar(tipo_cuidado)}")))'
                   ))


def get_mascotas_por_frecuencia_cuidado(frecuencia: str):
    return _salida(["Nombre", "Raza", "Frecuencia"],
                   _base_mascota(
                       select_extras="(STR(?frecuenciaCuidado) AS ?frecuencia)",
                       triples_extra="?mascota :requiereCuidado ?cuidadoObj . ?cuidadoObj :frecuenciaCuidado ?frecuenciaCuidado .",
                       filtro=f'FILTER(CONTAINS(LCASE(?frecuenciaCuidado), LCASE("{_sanitizar(frecuencia)}")))'
                   ))


def get_info_completa_mascota(nombre: str):
    return _salida(
        ["Nombre", "Edad", "Peso", "Color", "Sexo", "Raza", "Especie", "Due\u00f1o", "Alimento"],
        f"""
    {_PREF}
    SELECT DISTINCT 
           (STR(?nombreMascota) AS ?nombre) 
           (STR(?edadMascota) AS ?edad)
           (STR(?pesoMascota) AS ?peso)
           (STR(?colorMascota) AS ?color)
           (STR(?sexoMascota) AS ?sexo)
           (STR(?nombreRaza) AS ?raza)
           (STR(?nombreEspecie) AS ?especie)
           (STR(?nombreDue\u00f1o) AS ?due\u00f1o)
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
      OPTIONAL {{ ?mascota :tieneDue\u00f1o ?due\u00f1oObj . ?due\u00f1oObj :nombreDue\u00f1o ?nombreDue\u00f1o . }}
      OPTIONAL {{ ?mascota :consume ?alimentoObj . ?alimentoObj :marcaAlimento ?marcaAlimento . }}
      FILTER(CONTAINS(LCASE(?nombreMascota), LCASE("{_sanitizar(nombre)}")))
    }}
    """)


def get_todas_las_raza():
    return _salida(["Raza", "Especie"],
                   f"""
    {_PREF}
    SELECT (STR(?nombreRaza) AS ?raza) (STR(?nombreEspecie) AS ?especie)
    WHERE {{
      ?razaInd :perteneceAEspecie ?especieInd .
      ?razaInd :nombreRaza ?nombreRaza .
      ?especieInd :nombreEspecie ?nombreEspecie .
    }}
    ORDER BY ?especie ?raza
    """)


def get_mascotas_por_especie(especie: str):
    uri = ":Especie2" if especie.lower() == "perro" else ":Especie1"
    return _salida(["Nombre", "Raza"],
                   _base_mascota(
                       triples_extra=f"?razaObj :perteneceAEspecie {uri} ."
                   ))


def get_info_completa_por_especie(especie: str):
    uri = ":Especie2" if especie.lower() == "perro" else ":Especie1"
    return _salida(
        ["Nombre", "Edad", "Peso", "Color", "Raza", "Due\u00f1o", "Alimento"],
        f"""
    {_PREF}
    SELECT (STR(?nombreMascota) AS ?nombre) 
           (STR(?edadMascota) AS ?edad)
           (STR(?pesoMascota) AS ?peso)
           (STR(?colorMascota) AS ?color)
           (STR(?nombreRaza) AS ?raza)
           (STR(?nombreDue\u00f1o) AS ?due\u00f1o)
           (STR(?marcaAlimento) AS ?alimento)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :edadMascota ?edadMascota .
      ?mascota :pesoMascota ?pesoMascota .
      ?mascota :colorMascota ?colorMascota .
      ?mascota :tieneRaza ?raza .
      ?raza :nombreRaza ?nombreRaza .
      ?raza :perteneceAEspecie {uri} .
      OPTIONAL {{ ?mascota :tieneDue\u00f1o ?due\u00f1oObj . ?due\u00f1oObj :nombreDue\u00f1o ?nombreDue\u00f1o . }}
      OPTIONAL {{ ?mascota :consume ?alimentoObj . ?alimentoObj :marcaAlimento ?marcaAlimento . }}
    }}
    ORDER BY ?nombre
    """)
