from functools import lru_cache

from .sparql import (
    get_todas_las_mascotas,
    buscar_por_nombre_mascota,
    buscar_por_raza,
    get_mascotas_con_dueno,
    get_mascotas_por_edad,
    get_mascotas_por_alimento,
    get_todas_las_raza,
    get_info_completa_mascota,
    get_todos_los_perros,
    get_todos_los_gatos,
    get_info_completa_perros,
    get_info_completa_gatos
)
from .nlp.intent_parser import parse_intent
from .nlp.sparql_builder import build_sparql


@lru_cache(maxsize=1)
def get_todas():
    return get_todas_las_mascotas()


@lru_cache(maxsize=1)
def get_perros():
    return get_todos_los_perros()


@lru_cache(maxsize=1)
def get_gatos():
    return get_todos_los_gatos()


@lru_cache(maxsize=1)
def get_razas():
    return get_todas_las_raza()


def get_contar_duenos():
    resultados = get_mascotas_con_dueno()
    return len(resultados)


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
        return get_todos_los_perros()
    elif "gato" in q:
        return get_todos_los_gatos()
    return []


def _buscar_por_nombre_dueno(q: str):
    resultados = get_mascotas_con_dueno()
    return [r for r in resultados if q.lower() in r.get("Dueño", "").lower()]


def _buscar_por_alimento(q: str):
    return get_mascotas_por_alimento(q)


def buscar_avanzado(texto: str) -> list:
    intent = parse_intent(texto)
    tiene_intencion = any([
        intent.especie, intent.raza, intent.alimento, intent.dueno,
        intent.accesorio, intent.pelaje, intent.terminos_libres,
        intent.edad is not None, intent.sin_dueno
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


def info_mascota(nombre: str):
    return get_info_completa_mascota(nombre)


def info_perros():
    return get_info_completa_perros()


def info_gatos():
    return get_info_completa_gatos()