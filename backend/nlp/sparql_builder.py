from backend.sparql import (
    get_todas_las_mascotas,
    get_todos_los_perros,
    get_todos_los_gatos,
    get_mascotas_con_dueno,
    get_mascotas_sin_dueno,
    get_mascotas_por_edad,
    get_mascotas_por_alimento,
    get_mascotas_por_pelaje,
    get_mascotas_por_accesorio,
    buscar_por_raza,
    buscar_por_nombre_mascota,
)
from functools import lru_cache
from backend.nlp.intent_parser import Intent


def _filtro_por_terminos_libres(resultados: list, terminos: list) -> list:
    if not terminos:
        return resultados
    # collect all (Nombre, Raza) pairs that match ANY term, per term build a set
    term_sets = []
    for termino in terminos:
        termino = termino.lower()
        por_nombre = buscar_por_nombre_mascota(termino)
        por_raza = buscar_por_raza(termino)
        s = set()
        for r in por_nombre + por_raza:
            s.add((r.get("Nombre", "").lower(), r.get("Raza", "").lower()))
        if not s:
            return []
        term_sets.append(s)
    # intersect all term sets
    final = term_sets[0]
    for s in term_sets[1:]:
        final = final & s
    if not final:
        return []
    return [r for r in resultados
            if (r.get("Nombre", "").lower(), r.get("Raza", "").lower()) in final]


def build_sparql(intent: Intent) -> list:
    _limpiar_terminos(intent)
    if intent.accion == "contar":
        return _contar(intent)

    resultados = _build(intent)
    seen = set()
    unique = []
    for r in resultados:
        key = str(r.get("Nombre", "")) + str(r.get("Raza", ""))
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def _contar(intent: Intent) -> list:
    resultados = _build(intent)
    total = len(resultados)
    return [{"Total": total}]


def _limpiar_terminos(intent: Intent):
    valores_usados = set()
    if intent.especie:
        valores_usados.add(intent.especie.lower())
    if intent.raza:
        valores_usados.add(intent.raza.lower())
    if intent.alimento:
        valores_usados.add(intent.alimento.lower())
    if intent.dueno:
        valores_usados.add(intent.dueno.lower())
    if intent.accesorio:
        valores_usados.add(intent.accesorio.lower())
    if intent.pelaje:
        valores_usados.add(intent.pelaje.lower())
    intent.terminos_libres = [
        t for t in intent.terminos_libres
        if t.lower() not in valores_usados
    ]


def _build(intent: Intent) -> list:
    conjuntos = []

    if intent.accion == "listar" and not intent.especie and not intent.raza \
            and not intent.alimento and not intent.dueno and not intent.sin_dueno:
        todas = get_todas_las_mascotas()
        if intent.terminos_libres:
            todas = _filtro_por_terminos_libres(todas, intent.terminos_libres)
        return todas

    if intent.especie == "Perro":
        conjuntos.append(get_todos_los_perros())
    elif intent.especie == "Gato":
        conjuntos.append(get_todos_los_gatos())
    else:
        conjuntos.append(get_todas_las_mascotas())

    if intent.raza:
        conjuntos.append(buscar_por_raza(intent.raza))

    if intent.alimento:
        conjuntos.append(get_mascotas_por_alimento(intent.alimento))

    if intent.dueno:
        dueno_q = intent.dueno.lower()
        todas_con_dueno = get_mascotas_con_dueno()
        filtradas = [r for r in todas_con_dueno if dueno_q in str(r.get("Dueño", "")).lower()]
        conjuntos.append(filtradas)

    if intent.edad is not None:
        conjuntos.append(get_mascotas_por_edad(intent.edad))

    if intent.accesorio:
        conjuntos.append(get_mascotas_por_accesorio(intent.accesorio))

    if intent.pelaje:
        conjuntos.append(get_mascotas_por_pelaje(intent.pelaje))

    if intent.sin_dueno:
        conjuntos.append(get_mascotas_sin_dueno())

    if not conjuntos:
        return get_todas_las_mascotas()

    resultado_base = conjuntos[0]
    for otro in conjuntos[1:]:
        base_keyed = {}
        for r in resultado_base:
            key = (r.get("Nombre", "").lower(), r.get("Raza", "").lower())
            base_keyed[key] = r
        interseccion = []
        for r in otro:
            key = (r.get("Nombre", "").lower(), r.get("Raza", "").lower())
            if key in base_keyed:
                combinado = dict(base_keyed[key])
                combinado.update(r)
                interseccion.append(combinado)
        resultado_base = interseccion

    if intent.terminos_libres and resultado_base:
        resultado_base = _filtro_por_terminos_libres(resultado_base, intent.terminos_libres)

    return resultado_base
