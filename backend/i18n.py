TRADUCCIONES = {
    "Perro": {"en": "Dog", "es": "Perro", "port": "cão"},
    "Gato": {"en": "Cat", "es": "Gato"},
    "Nombre": {"en": "Name", "es": "Nombre"},
    "Raza": {"en": "Breed", "es": "Raza"},
    "Especie": {"en": "Species", "es": "Especie"},
    "Edad": {"en": "Age", "es": "Edad"},
    "Peso": {"en": "Weight", "es": "Peso"},
    "Color": {"en": "Color", "es": "Color"},
    "Sexo": {"en": "Sex", "es": "Sexo"},
    "Dueño": {"en": "Owner", "es": "Dueño"},
    "Alimento": {"en": "Food", "es": "Alimento"},
    "Accesorio": {"en": "Accessory", "es": "Accesorio"},
    "Cuidado": {"en": "Care", "es": "Cuidado"},
    "Pelaje": {"en": "Coat", "es": "Pelaje"},
    "Mascota": {"en": "Pet", "es": "Mascota"},
    "Tipo": {"en": "Type", "es": "Tipo"},
    "Mascotas": {"en": "Pets", "es": "Mascotas"},
    "Total": {"en": "Total", "es": "Total"},
    "Inicio": {"en": "Home", "es": "Inicio"},
    "Perros": {"en": "Dogs", "es": "Perros"},
    "Gatos": {"en": "Cats", "es": "Gatos"},
    "Razas": {"en": "Breeds", "es": "Razas"},
    "Dueños": {"en": "Owners", "es": "Dueños"},
    "Búsqueda Avanzada": {"en": "Advanced Search", "es": "Búsqueda Avanzada"},
    "Buscar Mascotas": {"en": "Search Pets", "es": "Buscar Mascotas"},
    "Información Completa": {"en": "Full Information", "es": "Información Completa"},
    "Sin Dueño": {"en": "Without Owner", "es": "Sin Dueño"},
    "Lista de Perros": {"en": "Dog List", "es": "Lista de Perros"},
    "Lista de Gatos": {"en": "Cat List", "es": "Lista de Gatos"},
    "Información desde DBpedia": {"en": "Information from DBpedia", "es": "Información desde DBpedia"},
    "No se encontraron resultados": {"en": "No results found", "es": "No se encontraron resultados"},
    "Origen": {"en": "Origin", "es": "Origen"},
    "Peso promedio": {"en": "Average weight", "es": "Peso promedio"},
    "Esperanza de vida": {"en": "Life expectancy", "es": "Esperanza de vida"},
    "Ver en DBpedia": {"en": "View on DBpedia", "es": "Ver en DBpedia"},
    "No disponible": {"en": "Not available", "es": "No disponible"},
    "Búsqueda Inteligente": {"en": "Intelligent Search", "es": "Búsqueda Inteligente"},
    "Escribe una frase completa para buscar mascotas": {"en": "Write a complete sentence to search for pets", "es": "Escribe una frase completa para buscar mascotas"},
    "Buscador Semántico de Mascotas": {"en": "Semantic Pet Search", "es": "Buscador Semántico de Mascotas"},
    "Total Mascotas": {"en": "Total Pets", "es": "Total Mascotas"},
    "Buscar por nombre, raza, especie...": {"en": "Search by name, breed, species...", "es": "Buscar por nombre, raza, especie..."},
    "Se encontraron": {"en": "Found", "es": "Se encontraron"},
    "resultado(s)": {"en": "result(s)", "es": "resultado(s)"},
    "Datos enriquecidos desde DBpedia (Linked Open Data)": {"en": "Enriched data from DBpedia (Linked Open Data)", "es": "Datos enriquecidos desde DBpedia (Linked Open Data)"},
    "Más información aquí": {"en": "More information here", "es": "Más información aquí"},
    "No se encontraron datos adicionales en DBpedia para estas razas.": {"en": "No additional data found in DBpedia for these breeds.", "es": "No se encontraron datos adicionales en DBpedia para estas razas."},
    "Error": {"en": "Error", "es": "Error"},
}

TRADUCCIONES_RAZA = {
    "Labrador": {"en": "Labrador Retriever", "es": "Labrador"},
    "Golden Retriever": {"en": "Golden Retriever", "es": "Golden Retriever"},
    "Bulldog": {"en": "Bulldog", "es": "Bulldog"},
    "Pastor Alemán": {"en": "German Shepherd", "es": "Pastor Alemán"},
    "Poodle": {"en": "Poodle", "es": "Poodle"},
    "Chihuahua": {"en": "Chihuahua", "es": "Chihuahua"},
    "Beagle": {"en": "Beagle", "es": "Beagle"},
    "Persa": {"en": "Persian", "es": "Persa"},
    "Siamés": {"en": "Siamese", "es": "Siamés"},
    "Maine Coon": {"en": "Maine Coon", "es": "Maine Coon"},
}


def t(texto: str, lang: str = "es") -> str:
    if texto in TRADUCCIONES and lang in TRADUCCIONES[texto]:
        return TRADUCCIONES[texto][lang]
    if texto in TRADUCCIONES_RAZA and lang in TRADUCCIONES_RAZA[texto]:
        return TRADUCCIONES_RAZA[texto][lang]
    return texto


def traducir_resultados(resultados: list, lang: str = "es") -> list:
    if lang == "es":
        return resultados
    traducidos = []
    for r in resultados:
        nuevo = {}
        for key, val in r.items():
            key_t = t(key, lang)
            val_t = t(str(val), lang) if isinstance(val, str) else val
            nuevo[key_t] = val_t
        traducidos.append(nuevo)
    return traducidos


def etiqueta_busqueda(termino: str, lang: str = "es") -> str:
    if lang == "es":
        return termino
    for es, traducciones in TRADUCCIONES.items():
        if traducciones.get("en", "").lower() == termino.lower():
            return traducciones["es"]
    for es, traducciones in TRADUCCIONES_RAZA.items():
        if traducciones.get("en", "").lower() == termino.lower():
            return traducciones["es"]
    return termino
