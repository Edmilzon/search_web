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


def _t(val, lang_map):
    """Return the capitalized Spanish string value for a trigger word.
    lang_map is a dict: word -> Spanish value (capitalized).
    Checks both text and lemma as keys."""
    if val in lang_map:
        return lang_map[val]
    return None


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

TRIGGER_ALIMENTO = {
    "come": "alimento", "comer": "alimento", "consume": "alimento", "consumir": "alimento",
    "alimento": "alimento", "alimenta": "alimento", "alimentación": "alimento",
    "marca": "alimento", "comida": "alimento",
    "eat": "alimento", "eats": "alimento", "eating": "alimento", "food": "alimento",
    "manger": "alimento", "nourriture": "alimento",
    "essen": "alimento", "fressen": "alimento", "futter": "alimento",
    "comer": "alimento", "comida": "alimento", "alimento": "alimento",
}

MARCAS_ALIMENTO = {"purina", "royal", "whiskas", "pedigree", "eukanuba", "pro plan", "hill's",
                   "acana", "orijen", "taste of the wild", "advance", "brit care", "diamond",
                   "canidae", "wellness", "applaws", "iams", "blue buffalo", "josera",
                   "nutragold", "nutra gold"}

TRIGGER_ACCION = {"todo": "listar", "todas": "listar", "todos": "listar",
                  "listar": "listar", "mostrar": "listar",
                  "dame": "listar",
                  "lista": "listar", "ver": "listar",
                  "cuántos": "contar", "cuantos": "contar",
                  "cuantas": "contar", "cuanta": "contar",
                  # English
                  "show": "listar", "list": "listar", "display": "listar",
                  "all": "listar",
                  "count": "contar", "how many": "contar",
                  # French
                  "montrer": "listar", "afficher": "listar", "lister": "listar",
                  "tous": "listar", "toutes": "listar",
                  "compter": "contar", "combien": "contar",
                  # German
                  "zeigen": "listar", "anzeigen": "listar", "auflisten": "listar",
                  "alle": "listar",
                  "zählen": "contar", "wie viele": "contar",
                  # Portuguese
                  "mostrar": "listar", "exibir": "listar", "listar": "listar",
                  "todos": "listar", "todas": "listar",
                  "contar": "contar", "quantos": "contar", "quantas": "contar",
                  }

TRIGGER_DUENO = {"dueño": "Dueño", "dueña": "Dueño", "dueno": "Dueño", "duena": "Dueño",
                 "propietario": "Dueño", "propietaria": "Dueño",
                 "dueños": "Dueño", "dueñas": "Dueño",
                 "owner": "Dueño", "owners": "Dueño",
                 # French
                 "propriétaire": "Dueño",
                 # German
                 "besitzer": "Dueño", "besitzerin": "Dueño",
                 # Portuguese
                 "dono": "Dueño", "dona": "Dueño", "proprietário": "Dueño", "proprietária": "Dueño",
                 }

TRIGGER_ACCESORIO = {
    # Spanish
    "collar": "Collar", "correa": "Correa", "juguete": "Juguete",
    "cama": "Cama", "comedero": "Comedero", "bebedero": "Bebedero",
    "arnés": "Arnés", "arnes": "Arnés", "transportadora": "Transportadora",
    "plato": "Plato", "rascador": "Rascador", "pelota": "Pelota",
    "cepillo": "Cepillo", "bozal": "Bozal", "manta": "Manta",
    "casa": "Casa", "jaula": "Jaula", "arenero": "Arenero",
    "correa retráctil": "Correa retráctil", "correa retractil": "Correa retráctil",
    "hueso de juguete": "Hueso de juguete", "ropa": "Ropa",
    # English
    "leash": "Correa", "toy": "Juguete", "bed": "Cama",
    "feeder": "Comedero", "drinker": "Bebedero",
    "harness": "Arnés", "carrier": "Transportadora",
    "plate": "Plato", "scratcher": "Rascador", "ball": "Pelota",
    "brush": "Cepillo", "muzzle": "Bozal", "blanket": "Manta",
    "house": "Casa", "cage": "Jaula", "litter box": "Arenero",
    "retractable leash": "Correa retráctil", "toy bone": "Hueso de juguete",
    "clothes": "Ropa",
    # French
    "laisse": "Correa", "jouet": "Juguete", "lit": "Cama",
    "mangeoire": "Comedero", "abreuvoir": "Bebedero",
    "harnais": "Arnés", "transporteur": "Transportadora",
    "assiette": "Plato", "grattoir": "Rascador", "balle": "Pelota",
    "brosse": "Cepillo", "muselière": "Bozal", "couverture": "Manta",
    "maison": "Casa", "cage": "Jaula", "bac à litière": "Arenero",
    # German
    "leine": "Correa", "spielzeug": "Juguete", "bett": "Cama",
    "futterautomat": "Comedero", "tränke": "Bebedero",
    "geschirr": "Arnés", "transportbox": "Transportadora",
    "teller": "Plato", "kratzbaum": "Rascador", "ball": "Pelota",
    "bürste": "Cepillo", "maulkorb": "Bozal", "decke": "Manta",
    "haus": "Casa", "käfig": "Jaula", "katzenklo": "Arenero",
    # Portuguese
    "guia": "Correa", "brinquedo": "Juguete", "cama": "Cama",
    "comedouro": "Comedero", "bebedouro": "Bebedero",
    "arreio": "Arnés", "transportadora": "Transportadora",
    "prato": "Plato", "arranhador": "Rascador", "bola": "Pelota",
    "escova": "Cepillo", "focinheira": "Bozal", "cobertor": "Manta",
    "casa": "Casa", "gaiola": "Jaula", "caixa de areia": "Arenero",
}

TRIGGER_PELAJE = {
    "corto": "Corto", "largo": "Largo", "rizado": "Rizado", "liso": "Liso",
    "short": "Corto", "long": "Largo", "curly": "Rizado", "straight": "Liso",
    "court": "Corto", "long": "Largo", "bouclé": "Rizado", "lisse": "Liso",
    "kurz": "Corto", "kurze": "Corto", "kurzer": "Corto", "kurzes": "Corto",
    "lang": "Largo", "lange": "Largo", "langer": "Largo", "langes": "Largo",
    "lockig": "Rizado", "lockige": "Rizado", "lockiger": "Rizado",
    "glatt": "Liso", "glatte": "Liso", "glatter": "Liso",
    "curto": "Corto", "comprido": "Largo", "crespo": "Rizado", "liso": "Liso",
}

TRIGGER_CUIDADO = {
    # Spanish
    "baño": "Baño", "bano": "Baño", "baño medicado": "Baño medicado", "bano medicado": "Baño medicado",
    "vacunación": "Vacunación", "vacunacion": "Vacunación", "vacuna anual": "Vacuna anual",
    "veterinario": "Revisión veterinaria",
    "desparasitación": "Desparasitación", "desparasitacion": "Desparasitación",
    "peluquería": "Peluquería", "peluqueria": "Peluquería",
    "cepillado": "Cepillado",
    "corte de uñas": "Corte de uñas", "corte de unas": "Corte de uñas",
    "limpieza dental": "Limpieza dental",
    "revisión veterinaria": "Revisión veterinaria", "revision": "Revisión veterinaria",
    "ejercicio": "Ejercicio", "entrenamiento": "Entrenamiento",
    "higiene ocular": "Higiene ocular",
    "desinfección": "Desinfección", "desinfeccion": "Desinfección",
    "control de peso": "Control de peso",
    "chequeo general": "Chequeo general",
    # English
    "bath": "Baño", "medicated bath": "Baño medicado",
    "vaccination": "Vacunación", "annual vaccine": "Vacuna anual",
    "vet": "Revisión veterinaria", "veterinary": "Revisión veterinaria",
    "deworming": "Desparasitación",
    "grooming": "Peluquería",
    "brushing": "Cepillado",
    "nail cut": "Corte de uñas", "nail trimming": "Corte de uñas",
    "dental cleaning": "Limpieza dental",
    "checkup": "Revisión veterinaria", "check-up": "Revisión veterinaria",
    "exercise": "Ejercicio", "training": "Entrenamiento",
    "eye hygiene": "Higiene ocular",
    "disinfection": "Desinfección",
    "weight control": "Control de peso",
    "general checkup": "Chequeo general",
    # French
    "bain": "Baño", "bain médicamente": "Baño medicado",
    "vaccination": "Vacunación", "vaccin annuel": "Vacuna anual",
    "vétérinaire": "Revisión veterinaria",
    "vermifugation": "Desparasitación",
    "toilettage": "Peluquería",
    "brossage": "Cepillado",
    "coupe des ongles": "Corte de uñas",
    "nettoyage dentaire": "Limpieza dental",
    "contrôle": "Revisión veterinaria",
    "exercice": "Ejercicio",
    "hygiène oculaire": "Higiene ocular",
    "désinfection": "Desinfección",
    "contrôle de poids": "Control de peso",
    # German
    "bad": "Baño", "medizinisches bad": "Baño medicado",
    "impfung": "Vacunación", "jährliche impfung": "Vacuna anual",
    "tierarzt": "Revisión veterinaria",
    "entwurmung": "Desparasitación",
    "pflege": "Peluquería",
    "bürsten": "Cepillado",
    "krallenschneiden": "Corte de uñas",
    "zahnreinigung": "Limpieza dental",
    "untersuchung": "Revisión veterinaria",
    "bewegung": "Ejercicio", "training": "Entrenamiento",
    "augenhygiene": "Higiene ocular",
    "desinfektion": "Desinfección",
    "gewichtskontrolle": "Control de peso",
    # Portuguese
    "banho": "Baño", "banho medicado": "Baño medicado",
    "vacinação": "Vacunación", "vacina anual": "Vacuna anual",
    "veterinário": "Revisión veterinaria",
    "desparasitação": "Desparasitación",
    "tosa": "Peluquería",
    "escovação": "Cepillado",
    "corte de unhas": "Corte de uñas",
    "limpeza dental": "Limpieza dental",
    "revisão": "Revisión veterinaria",
    "exercício": "Ejercicio", "treinamento": "Entrenamiento",
    "higiene ocular": "Higiene ocular",
    "desinfecção": "Desinfección",
    "controle de peso": "Control de peso",
}

TRIGGER_COLOR = {
    "blanco": "Blanco", "negro": "Negro", "marron": "Marrón", "marrón": "Marrón",
    "gris": "Gris", "dorado": "Dorado", "rojo": "Rojo",
    "azul": "Azul", "verde": "Verde", "naranja": "Naranja",
    "rosa": "Rosa", "violeta": "Violeta", "beige": "Beige", "crema": "Crema",
    "canela": "Canela", "chocolate": "Chocolate", "caramelo": "Caramelo",
    "miel": "Miel", "plateado": "Plateado", "cobrizo": "Cobrizo",
    "atigrado": "Atigrado", "bicolor": "Bicolor", "tricolor": "Tricolor",
    # English
    "white": "Blanco", "black": "Negro", "brown": "Marrón",
    "gray": "Gris", "grey": "Gris", "golden": "Dorado", "red": "Rojo",
    "blue": "Azul", "green": "Verde", "orange": "Naranja",
    "pink": "Rosa", "purple": "Violeta",
    "cream": "Crema", "cinnamon": "Canela",
    "honey": "Miel", "silver": "Plateado", "copper": "Cobrizo",
    "tabby": "Atigrado",
    # French
    "blanc": "Blanco", "noir": "Negro", "brun": "Marrón", "marron": "Marrón",
    "gris": "Gris", "doré": "Dorado", "rouge": "Rojo",
    "bleu": "Azul", "vert": "Verde",
    "rose": "Rosa",
    "crème": "Crema",
    # German
    "weiß": "Blanco", "schwarz": "Negro", "schwarze": "Negro", "schwarzer": "Negro", "schwarzes": "Negro",
    "braun": "Marrón", "braune": "Marrón", "brauner": "Marrón",
    "grau": "Gris", "golden": "Dorado", "rot": "Rojo",
    "blau": "Azul", "grün": "Verde",
    "pink": "Rosa",
    "creme": "Crema",
    # Portuguese
    "branco": "Blanco", "preto": "Negro", "marrom": "Marrón",
    "cinza": "Gris", "dourado": "Dorado", "vermelho": "Rojo",
    "azul": "Azul", "verde": "Verde",
    "laranja": "Naranja",
    "rosa": "Rosa", "violeta": "Violeta",
    "creme": "Crema",
}

TRIGGER_SEXO = {
    "macho": "Macho", "hembra": "Hembra", "masculino": "Macho", "femenino": "Hembra",
    "male": "Macho", "female": "Hembra",
    "mâle": "Macho", "femelle": "Hembra",
    "männlich": "Macho", "weiblich": "Hembra",
    "macho": "Macho", "fêmea": "Hembra", "feminino": "Hembra",
}

TRIGGER_ESTERILIZADO = {
    "esterilizado": "Esterilizado", "esterilizada": "Esterilizado",
    "esterilizar": "Esterilizado",
    "castrado": "Esterilizado", "castrada": "Esterilizado", "castrar": "Esterilizado",
    "neutered": "Esterilizado", "spayed": "Esterilizado", "fixed": "Esterilizado",
    "stérilisé": "Esterilizado",
    "kastriert": "Esterilizado",
    "esterilizado": "Esterilizado", "castrado": "Esterilizado",
}

TRIGGER_BOZAL = {
    "bozal": "Bozal",
    "muzzle": "Bozal",
    "muselière": "Bozal",
    "maulkorb": "Bozal",
    "focinheira": "Bozal",
}

TRIGGER_TEMPERAMENTO = {
    "tranquilo": "Tranquilo", "tranquila": "Tranquilo",
    "agresivo": "Agresivo", "agresiva": "Agresivo",
    "jugueton": "Juguetón", "juguetón": "Juguetón", "juguetona": "Juguetón",
    "activo": "Activo", "activa": "Activo",
    "perezoso": "Perezoso", "perezosa": "Perezoso",
    "docil": "Dócil", "dócil": "Dócil",
    "cariñoso": "Cariñoso", "cariñosa": "Cariñoso",
    "independiente": "Independiente",
    "valiente": "Valiente",
    "alerta": "Alerta",
    "nervioso": "Nervioso", "nerviosa": "Nervioso",
    "protector": "Protector", "protectora": "Protector",
    "amigable": "Amigable", "amigables": "Amigable",
    "amable": "Amable", "amables": "Amable",
    "sociable": "Sociable", "sociables": "Sociable",
    "tímido": "Tímido", "timido": "Tímido", "tímida": "Tímido", "timida": "Tímido",
    # English
    "calm": "Tranquilo", "quiet": "Tranquilo",
    "aggressive": "Agresivo",
    "playful": "Juguetón",
    "active": "Activo", "energetic": "Activo",
    "lazy": "Perezoso",
    "docile": "Dócil", "gentle": "Dócil",
    "affectionate": "Cariñoso", "loving": "Cariñoso",
    "independent": "Independiente",
    "brave": "Valiente", "courageous": "Valiente",
    "alert": "Alerta",
    "nervous": "Nervioso", "anxious": "Nervioso",
    "protective": "Protector",
    "friendly": "Amigable",
    "kind": "Amable",
    "social": "Sociable", "outgoing": "Sociable",
    "shy": "Tímido", "timid": "Tímido",
}

TRIGGER_TIPO_ALIMENTO = {
    "seco": "Seco", "humedo": "Húmedo", "húmedo": "Húmedo",
    "natural": "Natural", "premium": "Premium",
    "dry": "Seco", "wet": "Húmedo",
    "sec": "Seco", "humide": "Húmedo",
    "trocken": "Seco", "nass": "Húmedo", "feucht": "Húmedo",
    "seco": "Seco", "molhado": "Húmedo", "úmido": "Húmedo",
}

TRIGGER_FRECUENCIA = {
    "diario": "Diario", "diaria": "Diario",
    "semanal": "Semanal",
    "mensual": "Mensual",
    "anual": "Anual",
    "daily": "Diario",
    "weekly": "Semanal",
    "monthly": "Mensual",
    "yearly": "Anual", "annual": "Anual",
    "quotidien": "Diario", "journalier": "Diario",
    "hebdomadaire": "Semanal",
    "mensuel": "Mensual",
    "annuel": "Anual",
    "täglich": "Diario",
    "wöchentlich": "Semanal",
    "monatlich": "Mensual",
    "jährlich": "Anual",
    "diariamente": "Diario",
    "semanalmente": "Semanal",
    "mensalmente": "Mensual",
    "anualmente": "Anual",
}

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
    # Avoid interpreting mascota names as dueño names
    from ..sparql import get_todas_las_mascotas
    _nombres_mascotas = {r.get("Nombre", "").lower() for r in get_todas_las_mascotas()}
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
            if nombre.lower() in _nombres_mascotas:
                continue
            if nombre.lower() not in {"perro", "perros", "gato", "gatos", "raza", "razas",
                                             "color", "pelaje", "cuidado", "alimento", "edad",
                                             "peso", "sexo", "macho", "hembra", "dueño", "dueños"}:
                intent.dueno = nombre
                for token in doc:
                    if token.text.lower() in (posible_nombre, "de", "del"):
                        tokens_usados.add(token.i)
                break

    # "dueño/owner [nombre]" pattern
    if intent.dueno is None:
        pat = r"(?:dueñ[oa]s?|duen[oa]s?|propietari[oa]s?|owners?)\s+(?:es\s+|se\s+llama\s+|llamad[ao]\s+)?([a-záéíóúñ]+)"
        m = re.search(pat, texto_lower)
        if m:
            candidate = m.group(1).strip()
            # Skip if candidate tokens are already used (e.g., by breed detection)
            candidate_tokens = {token.i for token in doc
                                if candidate in token.text.lower()}
            if not candidate_tokens & tokens_usados:
                intent.dueno = candidate.capitalize()
            for token in doc:
                if token.text.lower() in TRIGGER_DUENO:
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
        if lemma in TRIGGER_ALIMENTO or token.text.lower() in TRIGGER_ALIMENTO:
            tokens_usados.add(token.i)

    # Age/weight range detection: "mayor/menor de X años/kg"
    for token in doc:
        if token.like_num:
            try:
                valor = int(token.text.replace(',', '.'))
                if valor > 100:
                    continue
            except ValueError:
                try:
                    valor = float(token.text.replace(',', '.'))
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
                elif idx > 0 and doc[idx - 1].lemma_ in {"pesar", "peso"}:
                    if intent.peso is None and intent.peso_min is None:
                        intent.peso = float(valor)
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
        texto = token.text.lower()
        v = _t(lemma, TRIGGER_ACCESORIO) or _t(texto, TRIGGER_ACCESORIO)
        if v:
            intent.accesorio = v
            tokens_usados.add(token.i)
        v = _t(lemma, TRIGGER_PELAJE) or _t(texto, TRIGGER_PELAJE)
        if v:
            intent.pelaje = v
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
        texto = token.text.lower()
        v = _t(lemma, TRIGGER_COLOR) or _t(texto, TRIGGER_COLOR)
        if v:
            intent.color = v
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        texto = token.text.lower()
        v = _t(lemma, TRIGGER_SEXO) or _t(texto, TRIGGER_SEXO)
        if v:
            intent.sexo = v
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        texto = token.text.lower().rstrip('s')
        v = _t(lemma, TRIGGER_TEMPERAMENTO) or _t(texto, TRIGGER_TEMPERAMENTO)
        if v and intent.temperamento is None:
            intent.temperamento = v
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        texto = token.text.lower()
        v = _t(lemma, TRIGGER_TIPO_ALIMENTO) or _t(texto, TRIGGER_TIPO_ALIMENTO)
        if v:
            intent.tipo_alimento = v
            tokens_usados.add(token.i)
            break

    for token in doc:
        lemma = token.lemma_.lower()
        texto = token.text.lower()
        v = _t(lemma, TRIGGER_CUIDADO) or _t(texto, TRIGGER_CUIDADO)
        if v:
            if intent.cuidado is None:
                intent.cuidado = v
                tokens_usados.add(token.i)

    for token in doc:
        lemma = token.lemma_.lower()
        texto = token.text.lower()
        v = _t(lemma, TRIGGER_FRECUENCIA) or _t(texto, TRIGGER_FRECUENCIA)
        if v:
            intent.frecuencia_cuidado = v
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
            texto = token.text.lower()
            if _t(lemma, TRIGGER_ESTERILIZADO) or _t(texto, TRIGGER_ESTERILIZADO):
                intent.esterilizado = True
                tokens_usados.add(token.i)
                break

    if intent.requiere_bozal is None:
        for token in doc:
            lemma = token.lemma_.lower()
            texto = token.text.lower()
            if _t(lemma, TRIGGER_BOZAL) or _t(texto, TRIGGER_BOZAL):
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
