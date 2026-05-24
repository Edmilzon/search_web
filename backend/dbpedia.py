import urllib.request
import urllib.parse
from xml.etree import ElementTree as ET


DBPEDIA_ENDPOINT = "https://es.dbpedia.org/sparql"

_MAPA_RAZA = {
    # Perros
    "labrador": "Labrador_retriever",
    "golden": "Golden_retriever",
    "bulldog": "Bulldog",
    "pastor alemán": "Pastor_alemán",
    "pastor aleman": "Pastor_alemán",
    "poodle": "Caniche",
    "chihuahua": "Chihuahua_(perro)",
    "beagle": "Beagle",
    "rottweiler": "Rottweiler",
    "yorkshire": "Yorkshire_terrier",
    "boxer": "Boxer_(perro)",
    "doberman": "Dóberman",
    "husky": "Husky_siberiano",
    "shih tzu": "Shih_Tzu",
    "border collie": "Border_collie",
    "collie": "Collie",
    # Gatos
    "persa": "Gato_persa",
    "siames": "Siamés_(gato)",
    "siamés": "Siamés_(gato)",
    "maine coon": "Maine_Coon",
    "bengala": "Bengala_(gato)",
    "ragdoll": "Ragdoll",
    "british shorthair": "British_Shorthair",
    "british": "British_Shorthair",
    "esfinge": "Sphynx_(gato)",
    "azul ruso": "Azul_ruso",
    "abisinio": "Abisinio_(gato)",
    "angora": "Angora_turco",
}

# Map Spanish DBpedia property keys to output keys the frontend expects
MAPA_PROPIEDADES = {
    "origen": "origin",
    "peso": "weight",
    "esperanzaDeVida": "lifeSpan",
    "vida": "lifeSpan",
    "tamaño": "size",
    "tamano": "size",
    "altura": "height",
    "pelaje": "fur",
    "país": "origin",
    "pais": "origin",
    "región": "origin",
    "region": "origin",
    "difusión": "origin",
    "difusion": "origin",
}


def _ejecutar_sparql(query: str) -> list:
    params = urllib.parse.urlencode({"query": query, "format": "xml"})
    url = f"{DBPEDIA_ENDPOINT}?{params}"

    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/sparql-results+xml",
            "User-Agent": "Mozilla/5.0 (compatible; PetSearchBot/1.0)"
        })
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
    uri = f"http://es.dbpedia.org/resource/{nombre_dbpedia}"

    query = f"""
    SELECT DISTINCT ?prop ?val
    WHERE {{
        <{uri}> ?prop ?val .
        FILTER(STRSTARTS(STR(?prop), "http://es.dbpedia.org/property/"))
    }}
    LIMIT 60
    """

    raw = _ejecutar_sparql(query)

    if not raw:
        return []

    result = {"raza": raza,
              "dbpedia_url": uri.replace("http://es.dbpedia.org/resource/",
                                         "https://es.wikipedia.org/wiki/")}
    propiedades_vistas = set()

    for row in raw:
        prop_uri = row.get("prop", "")
        val = row.get("val", "").strip()
        if not val:
            continue
        key = prop_uri.rsplit("/", 1)[-1]
        if key in propiedades_vistas:
            continue
        propiedades_vistas.add(key)
        out_key = MAPA_PROPIEDADES.get(key)
        if out_key:
            # Extract readable label from DBpedia URIs
            if val.startswith("http://") or val.startswith("https://"):
                val = val.rstrip("/").rsplit("/", 1)[-1].replace("_", " ")
            result[out_key] = val

    return [result]


def consultar_varias_razas(razas: list) -> list:
    resultados = []
    for raza in razas:
        resultados.extend(consultar_raza(raza))
    return resultados
