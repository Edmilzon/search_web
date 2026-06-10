from ..sparql import (
    get_todas_las_mascotas,
    get_mascotas_por_especie,
    get_mascotas_con_dueno,
    get_mascotas_sin_dueno,
    get_mascotas_por_edad,
    get_mascotas_por_alimento,
    get_mascotas_por_pelaje,
    get_mascotas_por_accesorio,
    get_mascotas_por_color,
    get_mascotas_por_sexo,
    get_mascotas_por_esterilizado,
    get_mascotas_por_requiere_bozal,
    get_mascotas_por_temperamento,
    get_mascotas_por_tipo_alimento,
    get_mascotas_por_cuidado,
    get_mascotas_por_frecuencia_cuidado,
    buscar_por_raza,
    buscar_por_nombre_mascota,
    buscar_por_nombre_raza_exacto,
    buscar_por_nombre_dueno,
    get_mascotas_por_rango_edad,
    get_mascotas_por_rango_peso,
    get_mascotas_por_marca_accesorio,
    get_busqueda_universal,
)
from .intent_parser import Intent


def _filtro_por_terminos_libres(resultados: list, terminos: list) -> list:
    _skip = _DUENO_WORDS | _ACC_WORDS
    terminos = [t for t in terminos if t.lower() not in _skip
                and not any(sw.startswith(t.lower()) for sw in _skip)]
    if not terminos:
        return resultados
    term_sets = []
    for termino in terminos:
        termino = termino.lower()
        por_nombre = buscar_por_nombre_mascota(termino)
        por_raza = buscar_por_raza(termino)
        s = set()
        for r in por_nombre + por_raza:
            s.add((r.get("Nombre", "").lower(), r.get("Raza", "").lower()))
        if not s:
            continue
        term_sets.append(s)
    if not term_sets:
        return resultados
    final = term_sets[0]
    for s in term_sets[1:]:
        final = final & s
    if not final:
        return []
    return [r for r in resultados
            if (r.get("Nombre", "").lower(), r.get("Raza", "").lower()) in final]


def build_sparql(intent: Intent) -> list:
    """Parse intent into SPARQL intersection, return matching mascotas."""
    _limpiar_terminos(intent)
    if intent.accion == "contar":
        return _contar(intent)
    return _build(intent)


def _contar(intent: Intent) -> list:
    """Execute _build and return a single-row result with total count."""
    resultados = _build(intent)
    return [{"Total": len(resultados)}]


_CONTEXT_WORDS = {"sin", "no", "color", "pelaje", "esterilizado", "castrado", "bozal",
                  "macho", "hembra", "seco", "humedo", "húmedo",
                  "diario", "diaria", "semanal", "mensual", "anual",
                  "come", "comer", "consume", "consumir", "alimento", "alimenta",
                   "necesita", "necesitar", "requiere", "requerir",
                   "marca", "entre", "mayor", "menor", "más", "mas", "de", "del",
                   "años", "año", "kilos", "kilo", "kg", "peso", "edad",
                  "mascotas", "mascota", "perros", "perro", "gatos", "gato",
                  "animal", "animales", "buscar", "busca", "dame", "lista",
                  "listar", "mostrar", "ver", "quiero", "todos", "todas"}

_DUENO_WORDS = {"dueño", "dueña", "dueno", "duena", "dueños", "dueñas",
                "propietario", "propietaria", "propietarios", "propietarias"}
_ACC_WORDS = {"accesorios", "accesorio", "accesorios de mascotas"}
_CARE_WORDS = {"cuidado", "cuidados", "metodo de cuidado", "metodos de cuidado"}

_DUENO_WORDS = {"dueño", "dueña", "dueno", "duena", "dueños", "dueñas",
                "propietario", "propietaria", "propietarios", "propietarias"}


def _limpiar_terminos(intent: Intent):
    valores_usados = set()
    for attr in ("especie", "raza", "raza_exacta", "alimento", "dueno",
                 "accesorio", "marca_accesorio", "pelaje", "color", "sexo",
                 "temperamento", "tipo_alimento", "cuidado", "frecuencia_cuidado"):
        val = getattr(intent, attr, None)
        if val:
            valores_usados.add(val.lower())

    intent.terminos_libres = [
        t for t in intent.terminos_libres
        if len(t) >= 3
        and t.lower() not in valores_usados
        and t.lower() not in _CONTEXT_WORDS
        and not any(cw.startswith(t.lower()) for cw in _CONTEXT_WORDS)
    ]


def _build(intent: Intent) -> list:
    """Build SPARQL result sets per filter, intersect by (Nombre, Raza)."""
    conjuntos = []
    _sc = lambda v: v is not None
    has_filters = any([
        intent.especie, intent.raza, intent.raza_exacta,
        intent.alimento, intent.dueno, intent.sin_dueno,
        _sc(intent.edad), _sc(intent.edad_min), _sc(intent.peso), _sc(intent.peso_min),
        intent.accesorio, intent.marca_accesorio,
        intent.pelaje, intent.color, intent.sexo,
        intent.temperamento, intent.tipo_alimento,
        intent.cuidado, intent.frecuencia_cuidado,
        _sc(intent.esterilizado), _sc(intent.requiere_bozal),
    ])

    if not has_filters:
        if intent.terminos_libres:
            if any(t.lower() in _DUENO_WORDS for t in intent.terminos_libres):
                return get_mascotas_con_dueno()
            if any(t.lower() in _ACC_WORDS for t in intent.terminos_libres):
                otros = [t for t in intent.terminos_libres if t.lower() not in _ACC_WORDS]
                if otros:
                    return get_busqueda_universal(" ".join(otros))
                return get_busqueda_universal("")
            if any(t.lower() in _CARE_WORDS for t in intent.terminos_libres):
                otros = [t for t in intent.terminos_libres if t.lower() not in _CARE_WORDS]
                if otros:
                    return get_busqueda_universal(" ".join(otros))
                return get_busqueda_universal("")
            universal = get_busqueda_universal(intent.terminos_libres[0])
            for t in intent.terminos_libres[1:]:
                partial = get_busqueda_universal(t)
                univ_keys = {(r.get("Nombre",""), r.get("Raza","")) for r in universal}
                universal = [r for r in partial
                             if (r.get("Nombre",""), r.get("Raza","")) in univ_keys]
            return universal
        return get_todas_las_mascotas()

    conjuntos.append(get_busqueda_universal(""))
    if intent.especie == "Perro":
        conjuntos.append(get_mascotas_por_especie("Perro"))
    elif intent.especie == "Gato":
        conjuntos.append(get_mascotas_por_especie("Gato"))

    if intent.raza_exacta:
        conjuntos.append(buscar_por_raza(intent.raza_exacta))

    if intent.raza and intent.raza != intent.raza_exacta:
        conjuntos.append(buscar_por_raza(intent.raza))

    if intent.alimento:
        conjuntos.append(get_mascotas_por_alimento(intent.alimento))

    if intent.dueno:
        conjuntos.append(buscar_por_nombre_dueno(intent.dueno))

    if intent.edad is not None:
        conjuntos.append(get_mascotas_por_edad(intent.edad))

    if intent.edad_min is not None or intent.edad_max is not None:
        emin = intent.edad_min if intent.edad_min is not None else 0
        emax = intent.edad_max if intent.edad_max is not None else 999
        conjuntos.append(get_mascotas_por_rango_edad(emin, emax))

    if intent.peso is not None:
        conjuntos.append(get_mascotas_por_rango_peso(intent.peso, intent.peso))

    if intent.peso_min is not None or intent.peso_max is not None:
        pmin = intent.peso_min if intent.peso_min is not None else 0.0
        pmax = intent.peso_max if intent.peso_max is not None else 999.0
        conjuntos.append(get_mascotas_por_rango_peso(pmin, pmax))

    if intent.accesorio:
        conjuntos.append(get_mascotas_por_accesorio(intent.accesorio))

    if intent.marca_accesorio:
        conjuntos.append(get_mascotas_por_marca_accesorio(intent.marca_accesorio))

    if intent.pelaje:
        conjuntos.append(get_mascotas_por_pelaje(intent.pelaje))

    if intent.color:
        conjuntos.append(get_mascotas_por_color(intent.color))

    if intent.sexo:
        conjuntos.append(get_mascotas_por_sexo(intent.sexo))

    if intent.esterilizado is not None:
        conjuntos.append(get_mascotas_por_esterilizado(intent.esterilizado))

    if intent.requiere_bozal is not None:
        conjuntos.append(get_mascotas_por_requiere_bozal(intent.requiere_bozal))

    if intent.temperamento:
        conjuntos.append(get_mascotas_por_temperamento(intent.temperamento))

    if intent.tipo_alimento:
        conjuntos.append(get_mascotas_por_tipo_alimento(intent.tipo_alimento))

    if intent.cuidado:
        conjuntos.append(get_mascotas_por_cuidado(intent.cuidado))

    if intent.frecuencia_cuidado:
        conjuntos.append(get_mascotas_por_frecuencia_cuidado(intent.frecuencia_cuidado))

    if intent.sin_dueno:
        conjuntos.append(get_mascotas_sin_dueno())

    if not conjuntos:
        return get_todas_las_mascotas()

    resultado_base = conjuntos[0]
    for otro in conjuntos[1:]:
        base_keyed = {}
        for r in resultado_base:
            key = (r.get("Nombre", "").lower(), r.get("Raza", "").lower())
            if key not in base_keyed:
                base_keyed[key] = []
            base_keyed[key].append(r)
        interseccion = []
        for r in otro:
            key = (r.get("Nombre", "").lower(), r.get("Raza", "").lower())
            if key in base_keyed and base_keyed[key]:
                base_r = base_keyed[key].pop(0)
                combinado = dict(base_r)
                combinado.update(r)
                interseccion.append(combinado)
        resultado_base = interseccion

    if intent.terminos_libres and resultado_base:
        resultado_base = _filtro_por_terminos_libres(resultado_base, intent.terminos_libres)

    return resultado_base
