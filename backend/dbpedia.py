import urllib.request
import urllib.parse
from xml.etree import ElementTree as ET


DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

_MAPA_RAZA = {
    "labrador": "Labrador_Retriever",
    "golden": "Golden_Retriever",
    "bulldog": "Bulldog",
    "pastor alemán": "German_Shepherd",
    "poodle": "Poodle",
    "chihuahua": "Chihuahua_(dog)",
    "beagle": "Beagle",
    "rottweiler": "Rottweiler",
    "yorkshire": "Yorkshire_Terrier",
    "boxer": "Boxer_(dog)",
    "doberman": "Doberman",
    "husky": "Siberian_Husky",
    "shih tzu": "Shih_Tzu",
    "border collie": "Border_Collie",
    "collie": "Collie",
    "persa": "Persian_cat",
    "siames": "Siamese_cat",
    "siamés": "Siamese_cat",
    "maine coon": "Maine_Coon",
    "bengala": "Bengal_cat",
    "ragdoll": "Ragdoll",
    "british": "British_Shorthair",
    "esfinge": "Sphynx_cat",
    "azul ruso": "Russian_Blue",
    "abisinio": "Abyssinian_cat",
    "angora": "Turkish_Angora",
}


def _ejecutar_sparql(query: str) -> list:
    params = urllib.parse.urlencode({"query": query, "format": "xml"})
    url = f"{DBPEDIA_ENDPOINT}?{params}"

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/sparql-results+xml"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_bytes = resp.read()
        return _parse_sparql_results(xml_bytes)
    except Exception as e:
        print(f"DBpedia error: {e}")
        return []


def _parse_sparql_results(xml_bytes: bytes) -> list:
    root = ET.fromstring(xml_bytes)
    ns = {"sparql": "http://www.w3.org/2005/sparql-results#"}

    variables = [v.get("name") for v in root.findall(".//sparql:head/sparql:variable", ns)]
    resultados = []

    for result_elem in root.findall(".//sparql:results/sparql:result", ns):
        fila = {}
        for binding in result_elem.findall("sparql:binding", ns):
            var_name = binding.get("name")
            for child in binding:
                tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if tag in ("literal", "uri", "bnode"):
                    fila[var_name] = child.text or ""
        resultados.append(fila)

    return resultados


def consultar_raza(raza: str) -> list:
    nombre_dbpedia = _MAPA_RAZA.get(raza.lower().strip())
    if not nombre_dbpedia:
        return []

    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label ?abstract ?origin ?weight ?lifeSpan
    WHERE {{
        <http://dbpedia.org/resource/{nombre_dbpedia}> rdfs:label ?label .
        OPTIONAL {{ <http://dbpedia.org/resource/{nombre_dbpedia}> dbo:abstract ?abstract . }}
        OPTIONAL {{ <http://dbpedia.org/resource/{nombre_dbpedia}> dbp:origin ?origin . }}
        OPTIONAL {{ <http://dbpedia.org/resource/{nombre_dbpedia}> dbo:averageWeight ?weight . }}
        OPTIONAL {{ <http://dbpedia.org/resource/{nombre_dbpedia}> dbo:lifeSpan ?lifeSpan . }}
        FILTER(LANG(?label) = "en")
    }}
    LIMIT 5
    """

    raw = _ejecutar_sparql(query)
    for d in raw:
        d["raza"] = raza
        d["dbpedia_url"] = f"http://dbpedia.org/resource/{nombre_dbpedia}"
    return raw


def consultar_varias_razas(razas: list) -> list:
    resultados = []
    for raza in razas:
        resultados.extend(consultar_raza(raza))
    return resultados
