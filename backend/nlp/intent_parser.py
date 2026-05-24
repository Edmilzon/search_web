import spacy
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Intent:
    accion: str = "buscar"
    especie: Optional[str] = None
    raza: Optional[str] = None
    alimento: Optional[str] = None
    dueno: Optional[str] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    accesorio: Optional[str] = None
    pelaje: Optional[str] = None
    color: Optional[str] = None
    sexo: Optional[str] = None
    esterilizado: Optional[bool] = None
    requiere_bozal: Optional[bool] = None
    temperamento: Optional[str] = None
    tipo_alimento: Optional[str] = None
    cuidado: Optional[str] = None
    frecuencia_cuidado: Optional[str] = None
    sin_dueno: bool = False
    texto_original: str = ""
    terminos_libres: list = field(default_factory=list)


_nlp = None


def _obtener_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("es_core_news_sm")
    return _nlp


STOP_WORDS = {"el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del",
              "que", "en", "por", "con", "y", "a", "al", "para", "es", "se", "su",
              "hay", "todos", "todas", "todo"}

TRIGGER_ESPECIE = {"perro", "perros", "perra", "perras", "can", "canino", "canina",
                   "gato", "gatos", "gata", "gatas", "felino", "felina", "minino", "minina"}

TRIGGER_ALIMENTO = {"come", "comer", "consume", "consumir",
                     "alimento", "alimenta", "alimentaci\u00f3n", "marca"}

MARCAS_ALIMENTO = {"purina", "royal", "whiskas", "pedigree", "eukanuba", "pro plan", "hill's"}

TRIGGER_ACCION = {"todo": "listar", "todas": "listar", "todos": "listar",
                  "listar": "listar", "mostrar": "listar",
                  "dame": "listar",
                  "lista": "listar", "ver": "listar",
                  "cuántos": "contar", "cuantos": "contar",
                  "cuantas": "contar", "cuanta": "contar"}

TRIGGER_DUENO = {"dueño": "Dueño", "dueña": "Dueño", "dueno": "Dueño", "duena": "Dueño",
                 "propietario": "Dueño", "propietaria": "Dueño",
                 "dueños": "Dueño", "dueñas": "Dueño"}

TRIGGER_ACCESORIO = {"collar", "correa", "juguete"}

TRIGGER_PELAJE = {"corto", "largo", "rizado", "liso"}

TRIGGER_CUIDADO = {"baño", "vacunación", "veterinario", "desparasitación", "peluquería"}

TRIGGER_COLOR = {"blanco", "negro", "marron", "marrón", "gris", "dorado", "rojo",
                 "azul", "verde", "naranja", "rosa", "violeta", "beige", "crema",
                 "canela", "chocolate", "caramelo", "miel", "plateado", "cobrizo",
                 "atigrado", "bicolor", "tricolor"}

TRIGGER_SEXO = {"macho", "hembra", "masculino", "femenino"}

TRIGGER_ESTERILIZADO = {"esterilizado", "esterilizada", "esterilizar",
                        "castrado", "castrada", "castrar"}

TRIGGER_BOZAL = {"bozal"}

TRIGGER_TEMPERAMENTO = {"tranquilo", "tranquila", "agresivo", "agresiva",
                        "jugueton", "juguetón", "juguetona", "activo", "activa",
                        "perezoso", "perezosa", "docil", "dócil", "cariñoso",
                        "cariñosa", "cariñoso", "independiente", "valiente",
                        "alerta", "nervioso", "nerviosa", "protector", "protectora"}

TRIGGER_TIPO_ALIMENTO = {"seco", "humedo", "húmedo"}

TRIGGER_FRECUENCIA = {"diario", "diaria", "semanal", "mensual", "anual"}


def parse_intent(texto: str) -> Intent:
    intent = Intent(texto_original=texto)
    texto_lower = texto.lower().strip()
    if not texto_lower:
        return intent

    doc = _obtener_nlp()(texto_lower)

    lemmas = set()
    for token in doc:
        lemmas.add(token.lemma_)

    tokens_usados = set()

    if "sin" in lemmas and ("dueño" in lemmas or "dueno" in lemmas or "dueña" in lemmas):
        intent.sin_dueno = True
        for token in doc:
            t = token.text.lower()
            if t == "sin" or t in ("dueño", "dueña", "dueno", "duena"):
                tokens_usados.add(token.i)

    for token in doc:
        texto = token.text.lower()
        lemma = token.lemma_.lower()
        if texto in TRIGGER_ACCION:
            intent.accion = TRIGGER_ACCION[texto]
            tokens_usados.add(token.i)
            break
        if lemma in TRIGGER_ACCION:
            intent.accion = TRIGGER_ACCION[lemma]
            tokens_usados.add(token.i)
            break

    for token in doc:
        texto = token.text.lower()
        lemma = token.lemma_.lower()
        if texto in TRIGGER_ESPECIE or lemma in TRIGGER_ESPECIE:
            key = texto if texto in TRIGGER_ESPECIE else lemma
            if key in {"perro", "perros", "perra", "perras", "can", "canino", "canina"}:
                intent.especie = "Perro"
            else:
                intent.especie = "Gato"
            tokens_usados.add(token.i)
            break

    pat = r"(?:dueñ[oa]s?|duen[oa]s?|propietari[oa]s?)\s+(?:es\s+|se\s+llama\s+|llamad[ao]\s+)?([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)?)"
    m = re.search(pat, texto_lower)
    if m:
        intent.dueno = m.group(1).strip().capitalize()
        for token in doc:
            if token.text.lower() in ("dueño", "dueña", "dueno", "duena", "propietario", "propietaria", "dueños", "dueñas"):
                tokens_usados.add(token.i)
                break

    for chunk in doc.noun_chunks:
        chunk_lower = chunk.text.lower()
        for marca in MARCAS_ALIMENTO:
            if marca in chunk_lower:
                intent.alimento = marca.title()
                for t in chunk:
                    tokens_usados.add(t.i)
                break

    if intent.alimento is None:
        for token in doc:
            texto = token.text.lower()
            lemma = token.lemma_.lower()
            if texto in MARCAS_ALIMENTO or lemma in MARCAS_ALIMENTO:
                intent.alimento = token.text.capitalize()
                tokens_usados.add(token.i)
                break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_ALIMENTO:
            tokens_usados.add(token.i)

    for token in doc:
        if token.like_num:
            try:
                valor = int(token.text)
            except ValueError:
                continue
            idx = token.i
            if idx + 1 < len(doc) and doc[idx + 1].lemma_ in {"año", "años", "edad"}:
                intent.edad = valor
                tokens_usados.add(idx)
                tokens_usados.add(idx + 1)
            elif idx > 0 and doc[idx - 1].lemma_ in {"edad", "años", "año"}:
                intent.edad = valor
                tokens_usados.add(idx - 1)
                tokens_usados.add(idx)
            elif idx + 1 < len(doc) and doc[idx + 1].lemma_ in {"peso", "kilo", "kilos", "kg"}:
                intent.peso = float(token.text)
                tokens_usados.add(idx)
                tokens_usados.add(idx + 1)
            elif intent.edad is None and intent.peso is None:
                intent.edad = valor
                tokens_usados.add(idx)

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_ACCESORIO:
            intent.accesorio = lemma.capitalize()
            tokens_usados.add(token.i)
        if lemma in TRIGGER_PELAJE:
            intent.pelaje = lemma.capitalize()
            tokens_usados.add(token.i)

    if intent.pelaje and not intent.accesorio:
        for token in doc:
            if token.lemma_.lower() == "pelaje":
                tokens_usados.add(token.i)
                break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_COLOR:
            intent.color = lemma.capitalize()
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_SEXO:
            intent.sexo = lemma.capitalize()
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_TEMPERAMENTO:
            intent.temperamento = lemma.capitalize()
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_TIPO_ALIMENTO:
            intent.tipo_alimento = lemma.capitalize()
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_CUIDADO:
            intent.cuidado = lemma.capitalize()
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_FRECUENCIA:
            intent.frecuencia_cuidado = lemma.capitalize()
            tokens_usados.add(token.i)
            break

    # Detect negation patterns: "sin X" or "no X"
    for token in doc:
        t = token.text.lower()
        if t in ("sin", "no") and token.i + 1 < len(doc):
            nxt = doc[token.i + 1].lemma_.lower()
            if nxt in TRIGGER_ESTERILIZADO:
                intent.esterilizado = False
                tokens_usados.add(token.i)
                tokens_usados.add(token.i + 1)
            elif nxt in TRIGGER_BOZAL:
                intent.requiere_bozal = False
                tokens_usados.add(token.i)
                tokens_usados.add(token.i + 1)

    # Positive detection for esterilizado
    if intent.esterilizado is None:
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in TRIGGER_ESTERILIZADO:
                intent.esterilizado = True
                tokens_usados.add(token.i)
                break

    # Positive detection for bozal
    if intent.requiere_bozal is None:
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in TRIGGER_BOZAL:
                intent.requiere_bozal = True
                tokens_usados.add(token.i)
                break

    # Color context: mark "color" as used if a color was found
    if intent.color:
        for token in doc:
            if token.lemma_.lower() == "color":
                tokens_usados.add(token.i)
                break

    for token in doc:
        if token.i not in tokens_usados:
            t = token.text.lower().strip(".,;:!¿?()\"'")
            if t and t not in STOP_WORDS and not token.like_num:
                intent.terminos_libres.append(token.text)

    return intent
