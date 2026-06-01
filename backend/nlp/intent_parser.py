import spacy
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Intent:
    accion: str = "buscar"
    especie: Optional[str] = None
    raza: Optional[str] = None
    raza_exacta: Optional[str] = None
    alimento: Optional[str] = None
    dueno: Optional[str] = None
    edad: Optional[int] = None
    edad_min: Optional[int] = None
    edad_max: Optional[int] = None
    peso: Optional[float] = None
    peso_min: Optional[float] = None
    peso_max: Optional[float] = None
    accesorio: Optional[str] = None
    marca_accesorio: Optional[str] = None
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
              "hay", "todos", "todas", "todo", "hay", "cual", "cuales", "como",
              "qué", "que", "donde", "dónde", "cómo", "entre", "hasta", "desde"}

TRIGGER_ESPECIE_PERRO = {"perro", "perros", "perra", "perras", "can", "canino", "canina",
                         "hund", "hunde", "dog", "dogs",
                         "chien", "chiens", "cachorro", "cachorros", "cão", "cães"}
TRIGGER_ESPECIE_GATO = {"gato", "gatos", "gata", "gatas", "felino", "felina", "minino", "minina",
                         "katze", "katzen", "cat", "cats",
                         "chat", "chats"}
TRIGGER_ESPECIE = TRIGGER_ESPECIE_PERRO | TRIGGER_ESPECIE_GATO

TRIGGER_ALIMENTO = {"come", "comer", "consume", "consumir",
                     "alimento", "alimenta", "alimentación", "marca", "comida"}

MARCAS_ALIMENTO = {"purina", "royal", "whiskas", "pedigree", "eukanuba", "pro plan", "hill's",
                   "acana", "orijen", "taste of the wild", "advance", "brit care", "diamond",
                   "canidae", "wellness", "applaws", "iams", "blue buffalo", "josera",
                   "nutragold", "nutra gold"}

TRIGGER_ACCION = {"todo": "listar", "todas": "listar", "todos": "listar",
                  "listar": "listar", "mostrar": "listar",
                  "dame": "listar",
                  "lista": "listar", "ver": "listar",
                  "cuántos": "contar", "cuantos": "contar",
                  "cuantas": "contar", "cuanta": "contar"}

TRIGGER_DUENO = {"dueño": "Dueño", "dueña": "Dueño", "dueno": "Dueño", "duena": "Dueño",
                 "propietario": "Dueño", "propietaria": "Dueño",
                 "dueños": "Dueño", "dueñas": "Dueño"}

TRIGGER_ACCESORIO = {"collar", "correa", "juguete", "cama", "comedero", "bebedero",
                     "arnés", "arnes", "transportadora", "plato", "rascador", "pelota",
                     "cepillo", "bozal", "manta", "casa", "jaula", "arenero",
                     "correa retráctil", "correa retractil", "hueso de juguete", "ropa"}

TRIGGER_PELAJE = {"corto", "largo", "rizado", "liso"}

TRIGGER_CUIDADO = {"baño", "bano", "vacunación", "vacunacion", "veterinario", "desparasitación",
                   "desparasitacion", "peluquería", "peluqueria", "cepillado", "corte de uñas",
                   "corte de unas", "limpieza dental", "revisión veterinaria", "revision",
                   "ejercicio", "entrenamiento", "higiene ocular", "desinfección",
                   "desinfeccion", "control de peso", "chequeo general", "vacuna anual",
                   "baño medicado", "bano medicado"}

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
                        "cariñosa", "independiente", "valiente",
                        "alerta", "nervioso", "nerviosa", "protector", "protectora",
                        "amigable", "amigables", "amable", "amables",
                        "sociable", "sociables", "tímido", "timido", "tímida", "timida"}

TRIGGER_TIPO_ALIMENTO = {"seco", "humedo", "húmedo", "natural", "premium"}

TRIGGER_FRECUENCIA = {"diario", "diaria", "semanal", "mensual", "anual"}

RAZA_MAP = {
    "labrador": "Labrador Retriever", "labrador retriever": "Labrador Retriever",
    "golden": "Golden Retriever", "golden retriever": "Golden Retriever",
    "bulldog": "Bulldog Francés",
    "bulldog francés": "Bulldog Francés", "bulldog frances": "Bulldog Francés",
    "bulldogge": "Bulldog Francés", "bouledogue": "Bulldog Francés",
    "pastor alemán": "Pastor Alemán", "pastor aleman": "Pastor Alemán",
    "schäferhund": "Pastor Alemán", "schaeferhund": "Pastor Alemán",
    "berger allemand": "Pastor Alemán",
    "poodle": "Poodle", "caniche": "Poodle", "pudel": "Poodle",
    "chihuahua": "Chihuahua", "beagle": "Beagle",
    "rottweiler": "Rottweiler",
    "yorkshire": "Yorkshire Terrier", "yorkshire terrier": "Yorkshire Terrier",
    "boxer": "Boxer",
    "doberman": "Doberman", "dóberman": "Doberman", "dobermann": "Doberman",
    "husky": "Husky Siberiano", "husky siberiano": "Husky Siberiano",
    "shih tzu": "Shih Tzu",
    "akita": "Akita",
    "border collie": "Border Collie", "collie": "Border Collie",
    "persa": "Persa", "gato persa": "Persa", "perserkatze": "Persa",
    "siamés": "Siamés", "siames": "Siamés", "gato siamés": "Siamés",
    "siamkatze": "Siamés", "siamois": "Siamés", "chat siamois": "Siamés",
    "maine coon": "Maine Coon",
    "bengala": "Bengala", "gato bengala": "Bengala", "bengal": "Bengala",
    "ragdoll": "Ragdoll",
    "british shorthair": "British Shorthair", "british": "British Shorthair",
    "esfinge": "Esfinge", "sphynx": "Esfinge",
    "azul ruso": "Azul Ruso",
    "abisinio": "Abisinio",
    "scottish fold": "Scottish Fold",
    "angora": "Angora", "angora turco": "Angora",
    "savannah": "Savannah",
    "bombay": "Bombay",
    "noruego del bosque": "Noruego del Bosque",
    "birmano": "Birmano",
}
_RAZA_TRIGGERS = sorted(set(RAZA_MAP), key=len, reverse=True)
_RAZA_TRIGGER_SET = set(RAZA_MAP)


def _detectar_raza_por_texto(texto_lower: str) -> Optional[str]:
    for trigger in _RAZA_TRIGGERS:
        if trigger in texto_lower:
            return RAZA_MAP[trigger]
    return None


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
            if key in TRIGGER_ESPECIE_PERRO:
                intent.especie = "Perro"
            elif key in TRIGGER_ESPECIE_GATO:
                intent.especie = "Gato"
            tokens_usados.add(token.i)
            break

    # Breed detection (multi-word first, then single)
    raza_detectada = _detectar_raza_por_texto(texto_lower)
    if raza_detectada:
        intent.raza_exacta = raza_detectada
        for token in doc:
            t = token.text.lower()
            l = token.lemma_.lower()
            if t in _RAZA_TRIGGER_SET or l in _RAZA_TRIGGER_SET:
                tokens_usados.add(token.i)
                continue
            # Mark token if it's part of a multi-word breed trigger
            for breed in _RAZA_TRIGGER_SET:
                if len(breed) >= 3 and (breed in t or t in breed):
                    tokens_usados.add(token.i)
                    break

    # "de [dueño]" pattern: "mascotas de Carlos", "perros de Ana"
    patron_de = r"(?:de|del)\s+([A-Za-záéíóúñÁÉÍÓÚÑ]+)"
    for m in re.finditer(patron_de, texto_lower):
        posible_nombre = m.group(1).strip()
        # Skip if candidate tokens are already used
        cand_tokens = {token.i for token in doc
                       if posible_nombre.lower() in token.text.lower()}
        if cand_tokens & tokens_usados:
            continue
        nombre = posible_nombre.capitalize()
        if len(nombre) > 2 and nombre not in ("Del", "Los", "Las", "El", "La", "Un", "Una"):
            if nombre.lower() not in {"perro", "perros", "gato", "gatos", "raza", "razas",
                                            "color", "pelaje", "cuidado", "alimento", "edad",
                                            "peso", "sexo", "macho", "hembra", "dueño", "dueños"}:
                intent.dueno = nombre
                for token in doc:
                    if token.text.lower() in (posible_nombre, "de", "del"):
                        tokens_usados.add(token.i)
                break

    # "dueño [nombre]" pattern (existing)
    if intent.dueno is None:
        pat = r"(?:dueñ[oa]s?|duen[oa]s?|propietari[oa]s?)\s+(?:es\s+|se\s+llama\s+|llamad[ao]\s+)?([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)?)"
        m = re.search(pat, texto_lower)
        if m:
            candidate = m.group(1).strip()
            # Skip if candidate tokens are already used (e.g., by breed detection)
            candidate_tokens = {token.i for token in doc
                               if candidate in token.text.lower()}
            if not candidate_tokens & tokens_usados:
                intent.dueno = candidate.capitalize()
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

    # Age/weight range detection: "mayor/menor de X años/kg"
    for token in doc:
        if token.like_num:
            try:
                valor = int(token.text)
                if valor > 100:
                    continue
            except ValueError:
                try:
                    valor = float(token.text)
                except ValueError:
                    continue
            idx = token.i
            # Check "mayor de X años" or "menor de X años"
            if idx > 1 and doc[idx - 1].text.lower() == "de":
                prev_word = doc[idx - 2].text.lower() if idx - 2 >= 0 else ""
                next_words = ""
                if idx + 1 < len(doc):
                    next_words = doc[idx + 1].lemma_.lower()
                is_age = next_words in ("año", "años", "edad", "años de edad")
                is_weight = next_words in ("peso", "kilo", "kilos", "kg")
                if prev_word in ("mayor", "más", "mas", "mayor de"):
                    if is_age:
                        intent.edad_min = valor
                        tokens_usados.update(range(max(0, idx-2), min(len(doc), idx+2)))
                    elif is_weight:
                        intent.peso_min = float(valor)
                        tokens_usados.update(range(max(0, idx-2), min(len(doc), idx+2)))
                elif prev_word in ("menor", "menos"):
                    if is_age:
                        intent.edad_max = valor
                        tokens_usados.update(range(max(0, idx-2), min(len(doc), idx+2)))
                    elif is_weight:
                        intent.peso_max = float(valor)
                        tokens_usados.update(range(max(0, idx-2), min(len(doc), idx+2)))
                else:
                    pass
            else:
                if idx + 1 < len(doc) and doc[idx + 1].lemma_ in {"año", "años", "edad"}:
                    if intent.edad is None and intent.edad_min is None:
                        intent.edad = valor
                        tokens_usados.add(idx)
                        tokens_usados.add(idx + 1)
                elif idx > 0 and doc[idx - 1].lemma_ in {"edad", "años", "año"}:
                    if intent.edad is None and intent.edad_min is None:
                        intent.edad = valor
                        tokens_usados.add(idx - 1)
                        tokens_usados.add(idx)
                elif idx + 1 < len(doc) and doc[idx + 1].lemma_ in {"peso", "kilo", "kilos", "kg"}:
                    if intent.peso is None and intent.peso_min is None:
                        intent.peso = float(token.text)
                        tokens_usados.add(idx)
                        tokens_usados.add(idx + 1)
                elif intent.edad is None and intent.edad_min is None:
                    intent.edad = valor
                    tokens_usados.add(idx)

    # "entre X y Y años/kg"
    patron_entre = r"entre\s+(\d+)\s*(?:y|a)\s*(\d+)\s*(años|año|kilos|kilo|kg|peso)?"
    m = re.search(patron_entre, texto_lower)
    if m:
        val1, val2 = int(m.group(1)), int(m.group(2))
        unidad = m.group(3) if m.group(3) else ""
        if unidad in ("años", "año", "edad"):
            intent.edad_min = min(val1, val2)
            intent.edad_max = max(val1, val2)
        elif unidad in ("kilos", "kilo", "kg", "peso"):
            intent.peso_min = float(min(val1, val2))
            intent.peso_max = float(max(val1, val2))
        else:
            intent.edad_min = min(val1, val2)
            intent.edad_max = max(val1, val2)
        for token in doc:
            if token.text.lower() in ("entre", "y", "a") or token.like_num:
                tokens_usados.add(token.i)

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

    # "marca [nombre]" for accessory brand
    patron_marca = r"marca\s+([a-záéíóúñ]+)"
    m = re.search(patron_marca, texto_lower)
    if m:
        marca = m.group(1).strip().capitalize()
        if marca not in ("Alimento", "Accesorio", "Cuidado"):
            intent.marca_accesorio = marca
            for token in doc:
                if token.text.lower() in ("marca", m.group(1)):
                    tokens_usados.add(token.i)
                if token.lemma_.lower() in ("marca", m.group(1)):
                    tokens_usados.add(token.i)

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
        texto = token.text.lower()
        lemma = token.lemma_.lower()
        key = None
        if texto in TRIGGER_TEMPERAMENTO:
            key = lemma if lemma in TRIGGER_TEMPERAMENTO else texto.rstrip('s')
        elif lemma in TRIGGER_TEMPERAMENTO:
            key = lemma
        if key and intent.temperamento is None:
            intent.temperamento = key.capitalize()
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
            if intent.cuidado is None:
                intent.cuidado = lemma.capitalize()
                tokens_usados.add(token.i)

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in TRIGGER_FRECUENCIA:
            intent.frecuencia_cuidado = lemma.capitalize()
            tokens_usados.add(token.i)
            break

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

    if intent.esterilizado is None:
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in TRIGGER_ESTERILIZADO:
                intent.esterilizado = True
                tokens_usados.add(token.i)
                break

    if intent.requiere_bozal is None:
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in TRIGGER_BOZAL:
                intent.requiere_bozal = True
                tokens_usados.add(token.i)
                break

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
