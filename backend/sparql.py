from rdflib import Graph, URIRef, Literal, RDFS
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
_NS_MASCOTAS = "http://www.semanticweb.org/mascotas#"


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


def _base_mascota(select_extras: str = "", triples_extra: str = "",
                  filtro: str = "", orden: str = "?nombre") -> str:
    return f"""
    {_PREF}
    SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
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
    SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?nombreDue\u00f1o) AS ?due\u00f1o)
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


def buscar_por_nombre_raza_exacto(nombre: str) -> list:
    nombre_limpio = _sanitizar(nombre)
    return _salida(["Nombre", "Raza", "Especie"],
                   f"""
    {_PREF}
    SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
           (STR(?nombreEspecie) AS ?especie)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      ?razaObj :perteneceAEspecie ?especieObj .
      ?especieObj :nombreEspecie ?nombreEspecie .
      FILTER(LCASE(?nombreRaza) = "{nombre_limpio.lower()}")
    }}
    """)


def buscar_por_nombre_dueno(nombre: str) -> list:
    return _salida(["Nombre", "Raza", "Dueño"],
                   f"""
    {_PREF}
    SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
           (STR(?nombreDueño) AS ?dueño)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      ?mascota :tieneDueño ?dueñoObj .
      ?dueñoObj :nombreDueño ?nombreDueño .
      FILTER(CONTAINS(LCASE(?nombreDueño), LCASE("{_sanitizar(nombre)}")))
    }}
    """)


def get_mascotas_por_rango_edad(edad_min: int, edad_max: int) -> list:
    return _salida(["Nombre", "Raza", "Edad"],
                   _base_mascota(
                       select_extras="(STR(?edadMascota) AS ?edad)",
                       triples_extra="?mascota :edadMascota ?edadMascota .",
                       filtro=f"FILTER(?edadMascota >= {edad_min} && ?edadMascota <= {edad_max})"
                   ))


def get_mascotas_por_rango_peso(peso_min: float, peso_max: float) -> list:
    return _salida(["Nombre", "Raza", "Peso"],
                   _base_mascota(
                       select_extras="(STR(?pesoMascota) AS ?peso)",
                       triples_extra="?mascota :pesoMascota ?pesoMascota .",
                       filtro=f"FILTER(?pesoMascota >= {peso_min} && ?pesoMascota <= {peso_max})"
                   ))


def get_mascotas_por_marca_accesorio(marca: str) -> list:
    return _salida(["Nombre", "Raza", "Accesorio"],
                   _base_mascota(
                       select_extras="(STR(?nombreAccesorio) AS ?accesorio)",
                       triples_extra="?mascota :usa ?accesorioObj . ?accesorioObj :nombreAccesorio ?nombreAccesorio . ?accesorioObj :marcaAccesorio ?marcaAccesorio .",
                       filtro=f'FILTER(CONTAINS(LCASE(?marcaAccesorio), LCASE("{_sanitizar(marca)}")))'
                   ))


def get_busqueda_universal(termino: str) -> list:
    q = _sanitizar(termino)
    return _salida(
        ["Nombre", "Edad", "Peso", "Color", "Sexo", "Raza", "Especie", "Dueño", "Alimento",
         "Accesorio", "Tipo de Pelaje", "Temperamento", "Cuidado", "Frecuencia"],
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
           (STR(?nombreDueño) AS ?dueño)
           (STR(?marcaAlimento) AS ?alimento)
           (STR(?nombreAccesorio) AS ?accesorio)
           (STR(?tipoPelaje) AS ?tipo_pelaje)
           (STR(?temperamento) AS ?temperamento)
           (STR(?tipoCuidado) AS ?cuidado)
           (STR(?frecuenciaCuidado) AS ?frecuencia)
    WHERE {{
      ?mascota :nombreMascota ?nombreMascota .
      ?mascota :tieneRaza ?razaObj .
      ?razaObj :nombreRaza ?nombreRaza .
      OPTIONAL {{ ?mascota :edadMascota ?edadMascota . }}
      OPTIONAL {{ ?mascota :pesoMascota ?pesoMascota . }}
      OPTIONAL {{ ?mascota :colorMascota ?colorMascota . }}
      OPTIONAL {{ ?mascota :sexoMascota ?sexoMascota . }}
      OPTIONAL {{ ?mascota :esterilizado ?esterilizado . }}
      OPTIONAL {{ ?mascota :requiereBozal ?requiereBozal . }}
      OPTIONAL {{ ?mascota :tipoPelaje ?tipoPelaje . }}
      OPTIONAL {{ ?mascota :consume ?alimentoObj . ?alimentoObj :marcaAlimento ?marcaAlimento . }}
      OPTIONAL {{ ?mascota :usa ?accesorioObj . ?accesorioObj :nombreAccesorio ?nombreAccesorio . }}
      OPTIONAL {{ ?mascota :tieneDueño ?dueñoObj . ?dueñoObj :nombreDueño ?nombreDueño . }}
      OPTIONAL {{ ?razaObj :perteneceAEspecie ?especieObj . ?especieObj :nombreEspecie ?nombreEspecie . }}
      OPTIONAL {{ ?razaObj :temperamento ?temperamento . }}
      OPTIONAL {{ ?mascota :requiereCuidado ?cuidadoObj . ?cuidadoObj :tipoCuidado ?tipoCuidado . }}
      OPTIONAL {{ ?cuidadoObj :frecuenciaCuidado ?frecuenciaCuidado . }}
      FILTER(
        CONTAINS(LCASE(?nombreMascota), LCASE("{q}")) ||
        CONTAINS(LCASE(?nombreRaza), LCASE("{q}")) ||
        CONTAINS(LCASE(?nombreEspecie), LCASE("{q}")) ||
        CONTAINS(LCASE(?nombreDueño), LCASE("{q}")) ||
        CONTAINS(LCASE(?marcaAlimento), LCASE("{q}")) ||
        CONTAINS(LCASE(?nombreAccesorio), LCASE("{q}")) ||
        CONTAINS(LCASE(?tipoPelaje), LCASE("{q}")) ||
        CONTAINS(LCASE(?tipoCuidado), LCASE("{q}")) ||
        CONTAINS(LCASE(?frecuenciaCuidado), LCASE("{q}"))
      )
    }}
    ORDER BY ?nombre
    """)


# ── Ontology-driven i18n ────────────────────────────

_CLASE_URI_MAP = {
    "Perro": _NS_MASCOTAS + "Perro",
    "Gato": _NS_MASCOTAS + "Gato",
    "Raza": _NS_MASCOTAS + "Raza",
    "Dueño": _NS_MASCOTAS + "Dueño",
    "Mascota": _NS_MASCOTAS + "Mascota",
    "Especie": _NS_MASCOTAS + "Especie",
    "Accesorio": _NS_MASCOTAS + "Accesorio",
    "Alimento": _NS_MASCOTAS + "Alimento",
    "Cuidado": _NS_MASCOTAS + "Cuidado",
}

_UI_STRINGS = {
    "Inicio": {"en": "Home", "fr": "Accueil", "de": "Start", "pt": "Início"},
    "Perros": {"en": "Dogs", "fr": "Chiens", "de": "Hunde", "pt": "Cachorros"},
    "Gatos": {"en": "Cats", "fr": "Chats", "de": "Katzen", "pt": "Gatos"},
    "Razas": {"en": "Breeds", "fr": "Races", "de": "Rassen", "pt": "Raças"},
    "Dueños": {"en": "Owners", "fr": "Propriétaires", "de": "Besitzer", "pt": "Donos"},
    "Mascotas": {"en": "Pets", "fr": "Animaux de compagnie", "de": "Haustiere", "pt": "Animais de estimação"},
    "Total Mascotas": {"en": "Total Pets", "fr": "Total Animaux", "de": "Haustiere gesamt", "pt": "Total Animais"},
    "Buscador Semántico de Mascotas": {"en": "Semantic Pet Search", "fr": "Recherche sémantique d'animaux", "de": "Semantische Haustiersuche", "pt": "Buscador Semântico de Animais"},
    "Búsqueda Inteligente": {"en": "Intelligent Search", "fr": "Recherche intelligente", "de": "Intelligente Suche", "pt": "Busca Inteligente"},
    "Error al cargar estadísticas": {"en": "Error loading statistics", "fr": "Erreur de chargement des statistiques", "de": "Fehler beim Laden der Statistiken", "pt": "Erro ao carregar estatísticas"},
    "Escribe una frase completa para buscar mascotas": {"en": "Write a complete sentence to search for pets", "fr": "Écrivez une phrase complète pour rechercher des animaux", "de": "Schreiben Sie einen vollständigen Satz, um nach Haustieren zu suchen", "pt": "Escreva uma frase completa para procurar animais"},
    "Buscar por nombre, raza, especie...": {"en": "Search by name, breed, species...", "fr": "Rechercher par nom, race, espèce...", "de": "Suche nach Name, Rasse, Art...", "pt": "Pesquisar por nome, raça, espécie..."},
    "Buscar por nombre, raza, especie, color, dueño, edad, peso, accesorio, cuidado...": {"en": "Search by name, breed, species, color, owner, age, weight, accessory, care...", "fr": "Rechercher par nom, race, espèce, couleur, propriétaire, âge, poids, accessoire, soin...", "de": "Suche nach Name, Rasse, Art, Farbe, Besitzer, Alter, Gewicht, Zubehör, Pflege...", "pt": "Pesquisar por nome, raça, espécie, cor, dono, idade, peso, acessório, cuidado..."},
    "Se encontraron": {"en": "Found", "fr": "Trouvé(s)", "de": "Gefunden", "pt": "Encontrado(s)"},
    "resultado(s)": {"en": "result(s)", "fr": "résultat(s)", "de": "Ergebnis(se)", "pt": "resultado(s)"},
    "Error": {"en": "Error", "fr": "Erreur", "de": "Fehler", "pt": "Erro"},
    "Información desde DBpedia": {"en": "Information from DBpedia", "fr": "Informations depuis DBpedia", "de": "Informationen von DBpedia", "pt": "Informações da DBpedia"},
    "Datos enriquecidos desde DBpedia (Linked Open Data)": {"en": "Enriched data from DBpedia (Linked Open Data)", "fr": "Données enrichies depuis DBpedia (Linked Open Data)", "de": "Angereicherte Daten von DBpedia (Linked Open Data)", "pt": "Dados enriquecidos da DBpedia (Linked Open Data)"},
    "Más información aquí": {"en": "More information here", "fr": "Plus d'informations ici", "de": "Mehr Informationen hier", "pt": "Mais informações aqui"},
    "No se encontraron datos adicionales en DBpedia para estas razas.": {"en": "No additional data found in DBpedia for these breeds.", "fr": "Aucune donnée supplémentaire trouvée dans DBpedia pour ces races.", "de": "Keine zusätzlichen Daten in DBpedia für diese Rassen gefunden.", "pt": "Nenhum dado adicional encontrado na DBpedia para estas raças."},
    "No se encontraron resultados": {"en": "No results found", "fr": "Aucun résultat trouvé", "de": "Keine Ergebnisse gefunden", "pt": "Nenhum resultado encontrado"},
    "Nombre": {"en": "Name", "fr": "Nom", "de": "Name", "pt": "Nome"},
    "Edad": {"en": "Age", "fr": "Âge", "de": "Alter", "pt": "Idade"},
    "Peso": {"en": "Weight", "fr": "Poids", "de": "Gewicht", "pt": "Peso"},
    "Color": {"en": "Color", "fr": "Couleur", "de": "Farbe", "pt": "Cor"},
    "Sexo": {"en": "Sex", "fr": "Sexe", "de": "Geschlecht", "pt": "Sexo"},
    "Tipo de Pelaje": {"en": "Coat Type", "fr": "Type de pelage", "de": "Felltyp", "pt": "Tipo de Pelagem"},
    "Temperamento": {"en": "Temperament", "fr": "Tempérament", "de": "Temperament", "pt": "Temperamento"},
    "Frecuencia": {"en": "Frequency", "fr": "Fréquence", "de": "Häufigkeit", "pt": "Frequência"},
    "Tipo de Alimento": {"en": "Food Type", "fr": "Type d'aliment", "de": "Futtertyp", "pt": "Tipo de Alimento"},
    "Tipo": {"en": "Type", "fr": "Type", "de": "Typ", "pt": "Tipo"},
}

_t_cache = {}


def t(texto: str, lang: str = "es") -> str:
    if lang == "es":
        return texto
    key = (texto, lang)
    if key in _t_cache:
        return _t_cache[key]

    uri = _CLASE_URI_MAP.get(texto)
    if uri:
        grafo = cargar_ontologia()
        for label in grafo.objects(URIRef(uri), RDFS.label):
            if isinstance(label, Literal) and label.language == lang:
                val = str(label)
                _t_cache[key] = val
                return val

    if texto in _UI_STRINGS and lang in _UI_STRINGS[texto]:
        val = _UI_STRINGS[texto][lang]
        _t_cache[key] = val
        return val

    return texto
