from functools import lru_cache

from .sparql import (
    get_todas_las_mascotas,
    buscar_por_nombre_mascota,
    buscar_por_raza,
    get_mascotas_con_dueno,
    get_mascotas_por_alimento,
    get_mascotas_por_especie,
    get_info_completa_por_especie,
)
from .nlp.intent_parser import parse_intent
from .nlp.sparql_builder import build_sparql


@lru_cache(maxsize=1)
def get_todas():
    return get_todas_las_mascotas()


@lru_cache(maxsize=1)
def get_perros():
    return get_mascotas_por_especie("Perro")


@lru_cache(maxsize=1)
def get_gatos():
    return get_mascotas_por_especie("Gato")


@lru_cache(maxsize=1)
def get_todos_duenos():
    return get_mascotas_con_dueno()


def get_contar_duenos():
    duenos = get_todos_duenos()
    return len(set(d["Due\u00f1o"] for d in duenos))


def buscar(query: str) -> list:
    query = query.strip()
    if not query:
        return []

    q = query.lower()
    resultados = []

    resultados += buscar_por_nombre_mascota(q)
    resultados += buscar_por_raza(q)
    resultados += _buscar_por_especie(q)
    resultados += _buscar_por_nombre_dueno(q)
    resultados += _buscar_por_alimento(q)

    seen = set()
    unique = []
    for r in resultados:
        key = r.get("Nombre", "") + r.get("Raza", "")
        if key and key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


def _buscar_por_especie(q: str):
    if "perro" in q:
        return get_mascotas_por_especie("Perro")
    elif "gato" in q:
        return get_mascotas_por_especie("Gato")
    return []


def _buscar_por_nombre_dueno(q: str):
    resultados = get_mascotas_con_dueno()
    return [r for r in resultados if q in r.get("Dueño", "").lower()]


def _buscar_por_alimento(q: str):
    return get_mascotas_por_alimento(q)


def buscar_avanzado(texto: str) -> list:
    intent = parse_intent(texto)
    tiene_intencion = any([
        intent.especie, intent.raza, intent.alimento, intent.dueno,
        intent.accesorio, intent.pelaje, intent.color, intent.sexo,
        intent.temperamento, intent.tipo_alimento, intent.cuidado,
        intent.frecuencia_cuidado, intent.terminos_libres,
        intent.edad is not None, intent.sin_dueno,
        intent.esterilizado is not None, intent.requiere_bozal is not None,
    ])
    if not tiene_intencion:
        return buscar(texto)
    return build_sparql(intent)


def enriquecer_con_dbpedia(resultados: list) -> list:
    from .dbpedia import consultar_varias_razas
    razas = set()
    for r in resultados:
        raza = r.get("Raza", "") or r.get("raza", "")
        if raza:
            razas.add(raza)
    if not razas:
        return []
    return consultar_varias_razas(list(razas))


@lru_cache(maxsize=1)
def info_perros():
    return get_info_completa_por_especie("Perro")


@lru_cache(maxsize=1)
def info_gatos():
    return get_info_completa_por_especie("Gato")