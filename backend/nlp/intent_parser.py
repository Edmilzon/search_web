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

TRIGGER_ESPECIE = {"perro", "perros", "can", "canino", "canina",
                   "gato", "gatos", "felino", "felina", "minino", "minina"}

TRIGGER_ALIMENTO = {"come", "comer", "comar", "consume", "consumir",
                    "alimento", "alimenta", "alimentaci\u00f3n", "marca"}

MARCAS_ALIMENTO = {"purina", "royal", "whiskas", "pedigree", "eukanuba", "pro plan", "hill's"}

TRIGGER_ACCION = {"todo": "listar", "todas": "listar", "todos": "listar",
                  "listar": "listar", "mostrar": "listar",
                  "dame": "listar", "damar": "listar",
                  "lista": "listar", "ver": "listar",
                  "cuántos": "contar", "cuantos": "contar",
                  "cuantas": "contar", "cuanta": "contar"}

TRIGGER_DUENO = {"dueño": "Dueño", "dueña": "Dueño", "dueno": "Dueño", "duena": "Dueño",
                 "propietario": "Dueño", "propietaria": "Dueño",
                 "dueños": "Dueño", "dueñas": "Dueño"}

TRIGGER_ACCESORIO = {"collar", "correa", "juguete", "accesorio"}

TRIGGER_PELAJE = {"corto", "largo", "rizado", "liso"}

TRIGGER_CUIDADO = {"baño", "vacunación", "veterinario", "cuidado"}


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
            if key in {"perro", "perros", "can", "canino", "canina"}:
                intent.especie = "Perro"
            else:
                intent.especie = "Gato"
            tokens_usados.add(token.i)
            break

    for nombre_clave in TRIGGER_DUENO:
        pat = rf"(?:dueñ[oa]s?|duen[oa]s?|propietari[oa]s?)\s+(?:es\s+|se\s+llama\s+|llamad[ao]\s+)?([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)?)"
        m = re.search(pat, texto_lower)
        if m:
            intent.dueno = m.group(1).strip().capitalize()
            for token in doc:
                if token.text.lower() in ("dueño", "dueña", "dueno", "duena", "propietario", "propietaria", "dueños", "dueñas"):
                    tokens_usados.add(token.i)
                    break
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
            valor = int(token.text)
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
        if token.i not in tokens_usados:
            t = token.text.lower().strip(".,;:!¿?()\"'")
            if t and t not in STOP_WORDS and not token.like_num:
                intent.terminos_libres.append(token.text)

    return intent
