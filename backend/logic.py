from .consultas import (
    get_todas_las_mascotas,
    buscar_por_nombre_mascota,
    buscar_por_raza,
    get_mascotas_con_dueno,
    get_mascotas_por_edad,
    get_mascotas_por_peso,
    get_mascotas_por_alimento,
    get_mascotas_por_tipo_alimento,
    get_mascotas_por_accesorio,
    get_mascotas_por_pelaje,
    get_todas_las_raza,
    get_info_completa_mascota,
    get_todos_los_perros,
    get_todos_los_gatos,
    get_info_completa_perros,
    get_info_completa_gatos
)


def buscar(query: str) -> list:
    query = query.strip()
    if not query:
        return []

    q = query.lower()
    resultados = []

    resultados += buscar_por_nombre_mascota(q)
    resultados += buscar_por_raza(q)
    resultados += buscar_por_especie(q)
    resultados += buscar_por_nombre_dueño(q)
    resultados += buscar_por_alimento(q)

    seen = set()
    unique = []
    for r in resultados:
        key = r.get("Nombre", "") + r.get("Raza", "")
        if key and key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


def buscar_por_nombre_mascota(q: str):
    from .consultas.mascotas import buscar_por_nombre_mascota as fn
    return fn(q)


def buscar_por_raza(q: str):
    from .consultas.mascotas import buscar_por_raza as fn
    return fn(q)


def buscar_por_especie(q: str):
    if "perro" in q:
        return get_todos_los_perros()
    elif "gato" in q:
        return get_todos_los_gatos()
    return []


def buscar_por_nombre_dueño(q: str):
    from .consultas.mascotas import get_mascotas_con_dueno as fn
    resultados = fn()
    return [r for r in resultados if q.lower() in r.get("Dueño", "").lower()]


def buscar_por_alimento(q: str):
    return get_mascotas_por_alimento(q)


def get_todas():
    return get_todas_las_mascotas()


def get_perros():
    return get_todos_los_perros()


def get_gatos():
    return get_todos_los_gatos()


def get_razas():
    return get_todas_las_raza()


def buscar_por_especie(especie: str):
    return buscar(especie)


def info_mascota(nombre: str):
    return get_info_completa_mascota(nombre)


def info_perros():
    return get_info_completa_perros()


def info_gatos():
    return get_info_completa_gatos()