# Defensa del Proyecto: Buscador Semántico de Mascotas

## Relación teoría ↔ implementación (archivos, líneas de código y conceptos)

---

## TEMA 1: Lenguajes para Web Semántica

### 1. HTML — Limitaciones (solo visualización, no describe datos)

**Teoría**: HTML está orientado a visualización, no permite describir datos, no es extensible.

**Implementación**: El proyecto NO usa HTML para representar datos. Usa **RDF/XML** en `database/mascotas.rdf`. HTML solo se usa para la interfaz visual (Streamlit + Bootstrap).

**Archivo**: `frontend/app.py:15-19` — Bootstrap CSS solo para estilos.
**Archivo**: `frontend/styles/main.css` — Solo apariencia visual (modo oscuro GitHub).

---

### 2. XML — Estructura jerárquica, extensible, espacios de nombres

**Teoría**: XML permite crear vocabularios propios, usa namespaces, es semi-estructurado.

**Implementación**: La ontología completa está serializada en RDF/XML.

**Archivo**: `database/mascotas.rdf:1-8`
```xml
<rdf:RDF xmlns="http://www.semanticweb.org/mascotas#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
```

- Namespaces: `rdf`, `owl`, `xsd`, `rdfs` (línea 4-8)
- Vocabulario propio: `:Mascota`, `:tieneRaza`, `:nombreMascota` (línea 1584-1600)
- Etiquetas creadas por el dominio: `<consume>`, `<tieneDueño>`, `<usa>`, `<tipoPelaje>` (línea 1586-1599)

---

### 3. RDF — Modelo de grafos, tripletas (Sujeto-Predicado-Objeto)

**Teoría**: RDF modela el mundo como un grafo dirigido etiquetado. Cada declaración es (sujeto, predicado, objeto).

**Implementación**: Cada individuo en la ontología es un conjunto de tripletas RDF.

**Archivo**: `database/mascotas.rdf:1584-1600`
```xml
<owl:NamedIndividual rdf:about="http://www.semanticweb.org/mascotas#Mascota1">
    <!-- Tripleta: Mascota1 rdf:type :Mascota -->
    <rdf:type rdf:resource="http://www.semanticweb.org/mascotas#Mascota"/>
    <!-- Tripleta: Mascota1 :tieneDueño :Dueño47 -->
    <tieneDueño rdf:resource="http://www.semanticweb.org/mascotas#Dueño47"/>
    <!-- Tripleta: Mascota1 :tieneRaza :Raza5 -->
    <tieneRaza rdf:resource="http://www.semanticweb.org/mascotas#Raza5"/>
    <!-- Tripleta: Mascota1 :nombreMascota "Bobby" -->
    <nombreMascota>Bobby</nombreMascota>
    <!-- Tripleta: Mascota1 :edadMascota 9 -->
    <edadMascota rdf:datatype="...integer">9</edadMascota>
</owl:NamedIndividual>
```

**Tripleta clásica**: `(Sujeto, Predicado, Objeto)`
- `(:Mascota1, :tieneRaza, :Raza5)` — objeto como URI
- `(:Mascota1, :nombreMascota, "Bobby")` — objeto como literal
- `(:Mascota1, :edadMascota, 9)` — objeto como literal tipado

**Cadena completa de relaciones**: `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`

**Archivo**: `backend/sparql.py:82-97` — plantilla base SPARQL que recorre estas tripletas:
```sparql
?mascota a :Mascota .                # rdf:type
?mascota :nombreMascota ?nombreMascota .
?mascota :tieneRaza ?razaObj .
?razaObj :nombreRaza ?nombreRaza .
```

---

### 4. RDF Schema — subClassOf, domain, range, jerarquía

**Teoría**: RDFS permite definir clases, subclases, dominio y rango de propiedades.

**Implementación**:

**subClassOf**: `database/mascotas.rdf:352-353` y `377-378`
```xml
<owl:Class rdf:about="http://www.semanticweb.org/mascotas#Gato">
    <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/mascotas#Especie"/>
</owl:Class>
<owl:Class rdf:about="http://www.semanticweb.org/mascotas#Perro">
    <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/mascotas#Especie"/>
</owl:Class>
```
- `Gato ⊑ Especie`, `Perro ⊑ Especie`

**domain/range en Object Properties**: `database/mascotas.rdf:26-29`
```xml
<owl:ObjectProperty rdf:about="http://www.semanticweb.org/mascotas#consume">
    <rdfs:domain rdf:resource="http://www.semanticweb.org/mascotas#Mascota"/>
    <rdfs:range rdf:resource="http://www.semanticweb.org/mascotas#Alimento"/>
</owl:ObjectProperty>
```
- `domain(consume) = Mascota`, `range(consume) = Alimento`

**domain/range en Datatype Properties**: `database/mascotas.rdf:119-122`
```xml
<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/mascotas#edadMascota">
    <rdfs:domain rdf:resource="http://www.semanticweb.org/mascotas#Mascota"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
</owl:DatatypeProperty>
```

**inverseOf**: `database/mascotas.rdf:53-54`
```xml
<owl:ObjectProperty rdf:about="http://www.semanticweb.org/mascotas#tieneDueño">
    <owl:inverseOf rdf:resource="http://www.semanticweb.org/mascotas#tieneMacota"/>
```

---

### 5. SPARQL — Lenguaje de consulta RDF

**Teoría**: Lenguaje de consulta para RDF. Ejemplo: "Pediatras de Santiago que atiendan por Fonasa" usando variables y tripletas.

**Implementación**: 27 funciones de consulta SPARQL.

**Motor**: RDFlib + OWL-RL — `backend/sparql.py:48-55` y `58-65`
```python
def cargar_ontologia(aplicar_razonamiento=True):
    grafo = Graph()
    grafo.parse(_ONTOLOGY_PATH, format="xml")
    DeductiveClosure(OWLRL_Semantics).expand(grafo)

def ejecutar_query(query: str) -> list:
    return list(grafo.query(query))
```

**Plantilla base**: `backend/sparql.py:82-97`
```sparql
SELECT DISTINCT (STR(?nombreMascota) AS ?nombre) (STR(?nombreRaza) AS ?raza)
WHERE {
  ?mascota a :Mascota .
  ?mascota :nombreMascota ?nombreMascota .
  ?mascota :tieneRaza ?razaObj .
  ?razaObj :nombreRaza ?nombreRaza .
}
```

**Funciones por tipo** (todas en `backend/sparql.py`):

| Consulta | Línea | Propósito |
|---|---|---|
| `get_todas_las_mascotas` | 104-106 | Todas las mascotas |
| `buscar_por_nombre_mascota` | 109-113 | Por nombre (substring) |
| `buscar_por_raza` | 116-120 | Por raza (substring) |
| `get_mascotas_con_dueno` | 123-136 | Con dueño |
| `get_mascotas_sin_dueno` | 139-143 | Sin dueño (`FILTER NOT EXISTS`) |
| `get_mascotas_por_edad` | 146-152 | Edad exacta |
| `get_mascotas_por_alimento` | 155-161 | Por marca de alimento |
| `get_mascotas_por_accesorio` | 164-170 | Por nombre de accesorio |
| `get_mascotas_por_pelaje` | 173-179 | Por tipo de pelaje |
| `get_mascotas_por_color` | 182-188 | Por color |
| `get_mascotas_por_sexo` | 191-197 | Por sexo |
| `get_mascotas_por_esterilizado` | 200-205 | Booleano |
| `get_mascotas_por_requiere_bozal` | 209-215 | Booleano |
| `get_mascotas_por_temperamento` | 218-224 | Por temperamento |
| `get_mascotas_por_tipo_alimento` | 227-233 | Tipo (seco/húmedo) |
| `get_mascotas_por_cuidado` | 236-242 | Por tipo de cuidado |
| `get_mascotas_por_frecuencia_cuidado` | 245-251 | Frecuencia |
| `get_mascotas_por_rango_edad` | 374-380 | Rango edad |
| `get_mascotas_por_rango_peso` | 383-389 | Rango peso |
| `get_mascotas_por_marca_accesorio` | 392-398 | Por marca |
| `get_busqueda_universal` | 401-452 | Búsqueda en todos los campos |

**Protección contra inyección**: `backend/sparql.py:14-15`
```python
def _sanitizar(valor):
    return _sin_acentos(re.sub(r'["\\]', '', str(valor)))
```

**Acentos-insensitive**: `backend/sparql.py:30-33`
```python
def _filtro_contains(columna: str, termino: str) -> str:
    return f'FILTER(CONTAINS({_col_sin_acentos(f"LCASE({columna})")}, LCASE("{q}")))'
```

---

### 6. URIs — Todo es un recurso identificable

**Teoría**: Páginas web, BD, etc. son recursos con URI.

**Implementación**: `database/mascotas.rdf:2-3`
```xml
xml:base="http://www.semanticweb.org/mascotas"
```
**Archivo**: `backend/sparql.py:44-45`
```python
_PREF = "PREFIX : <http://www.semanticweb.org/mascotas#>"
_NS_MASCOTAS = "http://www.semanticweb.org/mascotas#"
```

Cada individuo tiene su URI única:
- `http://www.semanticweb.org/mascotas#Mascota1` (línea 1584)
- `http://www.semanticweb.org/mascotas#Raza5`
- `http://www.semanticweb.org/mascotas#Dueño47`
- `http://www.semanticweb.org/mascotas#Especie1`

---

### 7. Herramientas — Protégé, Jena

**Teoría**: Protégé para crear ontologías, Jena como framework.

**Implementación**:
- **Protégé**: La ontología `database/mascotas.rdf` fue exportada desde Protégé (formato RDF/XML).
- **RDFlib**: `backend/sparql.py:1` — `from rdflib import Graph, URIRef, Literal, RDFS`
- **OWL-RL**: `backend/sparql.py:5` — `from owlrl import DeductiveClosure, OWLRL_Semantics`

---

## TEMA 2: Web Ontology Language (OWL)

### 8. OWL estándar W3C — Sintaxis RDF/XML

**Teoría**: OWL es el lenguaje de ontologías para la Web Semántica, parte de la pila W3C.

**Implementación**: `database/mascotas.rdf:4`
```xml
xmlns:owl="http://www.w3.org/2002/07/owl#"
```
- Uso de `owl:Class`, `owl:ObjectProperty`, `owl:DatatypeProperty`, `owl:NamedIndividual`, `owl:inverseOf`, `owl:Ontology`.

---

### 9. OWL-RL Reasoner — Inferencia automática

**Teoría**: Las ontologías permiten razonamiento automático. OWL tiene perfiles: OWL Lite, OWL DL, OWL Full, y sub-lenguajes como OWL-RL.

**Implementación**: `backend/sparql.py:48-55`
```python
def cargar_ontologia(aplicar_razonamiento=True):
    global _grafo_cache
    if _grafo_cache is None:
        _grafo_cache = Graph()
        _grafo_cache.parse(_ONTOLOGY_PATH, format="xml")
        if aplicar_razonamiento:
            DeductiveClosure(OWLRL_Semantics).expand(_grafo_cache)
    return _grafo_cache
```
Se aplica **OWL-RL** (perfil basado en reglas, tratable computacionalmente) que expande el grafo con tripletas inferidas. El grafo se cachea globalmente como singleton (proceso-vida).

**Impacto**: Al aplicar OWL-RL, el número de tripletas pasa de ~2370 a ~4111 (casi el doble), ya que el reasoner materializa inferencias como herencia de propiedades, dominios, rangos, etc.

---

### 10. Entidades: Individuos, Propiedades, Clases

**Teoría**: Tres tipos de entidades: Individuos (objetos), Propiedades (relaciones), Clases (conjuntos).

**Implementación**:

| Tipo | Ejemplos | Archivo | Líneas |
|---|---|---|---|
| **Clases** (9) | Mascota, Perro, Gato, Raza, Dueño, Especie, Accesorio, Alimento, Cuidado | `mascotas.rdf` | 290-396 |
| **Prop. Objeto** (6) | tieneRaza, tieneDueño, consume, usa, requiereCuidado, perteneceAEspecie | `mascotas.rdf` | 24-84 |
| **Prop. Dato** (16) | nombreMascota, edadMascota, pesoMascota, colorMascota, sexoMascota, tipoPelaje, nombreRaza, nombreDueño, nombreEspecie, marcaAlimento, tipoAlimento, nombreAccesorio, marcaAccesorio, tipoCuidado, frecuenciaCuidado, esterilizado, requiereBozal, esperanzaVida, edadDueño, temperamento | `mascotas.rdf` | 99-276 |
| **Individuos** (110) | Mascota1-Mascota110, Raza1-Raza30, Dueño1-Dueño50, etc. | `mascotas.rdf` | 411-4228 |

---

### 11. Axiomas: subClassOf, Jerarquía de clases, Taxonomía

**Teoría**: Con subClassOf obtenemos una jerarquía (taxonomía). Una clase puede tener varias superclases.

**Implementación**:
```
owl:Thing
├── Especie
│   ├── Perro (subClassOf Especie)
│   └── Gato  (subClassOf Especie)
├── Mascota
├── Raza
├── Dueño
├── Accesorio
├── Alimento
├── Cuidado
```

**Archivo**: `database/mascotas.rdf:352-353` y `377-378`
```xml
<owl:Class rdf:about="#Gato"><rdfs:subClassOf rdf:resource="#Especie"/></owl:Class>
<owl:Class rdf:about="#Perro"><rdfs:subClassOf rdf:resource="#Especie"/></owl:Class>
```

**Hardcodeo de especies**: `backend/sparql.py:303`
```python
uri = ":Especie2" if especie.lower() == "perro" else ":Especie1"
```
- `:Especie1` = Gato, `:Especie2` = Perro

---

### 12. OWA (Open World Assumption)

**Teoría**: En KB, lo omitido es desconocido (no falso). Se puede añadir nuevo conocimiento fácilmente.

**Implementación**: El proyecto implementa búsqueda con `OPTIONAL` en SPARQL:
`backend/sparql.py:272-282`
```sparql
OPTIONAL { ?mascota :edadMascota ?edadMascota . }
OPTIONAL { ?mascota :tieneDueño ?dueñoObj . ... }
```
Esto respeta OWA — si una mascota no tiene dueño registrado, no se asume que no tenga dueño, simplemente no se devuelve ese campo.

**⚠️ Ausente**: No se declaran `owl:differentFrom` entre individuos (no hay Unique Name Assumption). No hay restricciones OWL que limiten el modelo bajo OWA.

---

### 13. ❌ Restricciones OWL ausentes (debilidad identificada)

**Teoría**: OWL permite:
- `owl:someValuesFrom` (restricción existencial): `Humano ⊑ come some Planta`
- `owl:allValuesFrom` (restricción universal): `Humano ⊑ come only Organismo`
- `owl:hasValue` (valor concreto): `Humano ⊑ come value este_tomate`
- `owl:cardinality` (min/max/exact): `come min 1 Planta`
- `owl:intersectionOf`, `owl:unionOf`, `owl:complementOf`

**Implementación**: **NO existen** en `database/mascotas.rdf`. La ontología solo tiene:
- ✅ `rdfs:subClassOf` — jerarquía simple
- ✅ `rdfs:domain` / `rdfs:range` — restricciones de tipo
- ✅ `owl:inverseOf` — propiedad inversa
- ❌ Sin `owl:someValuesFrom`
- ❌ Sin `owl:allValuesFrom`
- ❌ Sin `owl:cardinality`
- ❌ Sin `owl:equivalentClass`
- ❌ Sin `owl:disjointWith`
- ❌ Sin `owl:intersectionOf` / `owl:unionOf`

**Posible pregunta**: "¿Por qué aplicar OWL-RL si no hay restricciones?"
**Respuesta**: El reasoner igualmente infiere tripletas de dominio/rango, herencia de propiedades, y tipos. Pero sin restricciones, el poder de inferencia es limitado.

---

### 14. ❌ Clases definidas (EquivalentClass) ausentes

**Teoría**: Clases con condiciones **necesarias y suficientes** se llaman definidas (ej: `Humano ≡ produce some Lenguaje`). Permiten clasificación automática.

**Implementación**: No hay `owl:equivalentClass` en la ontología. Todas las clases son **primitivas** (solo condiciones necesarias).

**Para defensa**: Se puede argumentar que el dominio (mascotas) es simple y no requiere clasificación automática compleja. Las 27 consultas SPARQL cubren todos los filtros necesarios.

---

### 15. ❌ Clases disjuntas (disjointWith) ausentes

**Teoría**: `owl:disjointWith` asegura que dos clases no compartan individuos.

**Implementación**: No hay `owl:disjointWith`. Por ejemplo, `Perro` y `Gato` no están declarados como disjuntos explícitamente (aunque por dominio tienen individuos separados).

---

## TEMA 3: Ontologías y Multilingualidad

### 16. Internacionalización — rdfs:label con xml:lang

**Teoría**: Proceso de generalizar un producto para múltiples lenguas y culturas sin rediseño.

**Implementación**: `database/mascotas.rdf:292-395` — 45 etiquetas `rdfs:label` para 9 clases en 5 idiomas:

```xml
<owl:Class rdf:about="#Perro">
    <rdfs:label xml:lang="en">Dog</rdfs:label>
    <rdfs:label xml:lang="fr">Chien</rdfs:label>
    <rdfs:label xml:lang="es">Perro</rdfs:label>
    <rdfs:label xml:lang="de">Hund</rdfs:label>
    <rdfs:label xml:lang="pt">Cachorro</rdfs:label>
</owl:Class>
```

Cada clase tiene etiquetas completas en **es, en, fr, de, pt**.

---

### 17. Función t() — Traducción RDF-backed

**Teoría**: Opción A de modelización — ampliar el metamodelo con información lingüística (etiquetas multi-idioma).

**Implementación**: `backend/sparql.py:506-527`
```python
def t(texto: str, lang: str = "es") -> str:
    if lang == "es":
        return texto                         # español por defecto
    uri = _CLASE_URI_MAP.get(texto)          # buscar en RDF
    if uri:
        for label in grafo.objects(URIRef(uri), RDFS.label):
            if label.language == lang:
                return str(label)
    if texto in _UI_STRINGS and lang in _UI_STRINGS[texto]:
        return _UI_STRINGS[texto][lang]       # fallback UI strings
    return texto
```

Flujo:
1. Si es español → devuelve texto original
2. Busca `rdfs:label` en el grafo RDF para clases de la ontología
3. Si no encuentra, busca en `_UI_STRINGS` (traducciones de UI)
4. Cachea en `_t_cache` para eficiencia

**Mapeo clase → URI**: `backend/sparql.py:457-467`
```python
_CLASE_URI_MAP = {
    "Perro": _NS_MASCOTAS + "Perro",
    "Gato": _NS_MASCOTAS + "Gato",
    "Raza": _NS_MASCOTAS + "Raza",
    "Dueño": _NS_MASCOTAS + "Dueño",
    ...
}
```

---

### 18. Nivel Interfaz — Mensajes multilingües no simultáneos

**Teoría**: Tres tipos: monolingüe, multilingüe simultáneo, multilingüe no simultáneo (selector de idioma).

**Implementación**: `frontend/app.py:36-56` — Selector de idioma tipo pills, **no simultáneo** (un idioma a la vez):
```python
if "lang" not in st.session_state:
    st.session_state.lang = "es"
lang = st.pills("Idioma", options=["es", "en", "fr", "de", "pt"], ...)
```

La selección se guarda en `st.session_state.lang` y se usa en toda la app.

**UI Strings**: `backend/sparql.py:469-501` — Diccionario `_UI_STRINGS` con traducciones para ~30 claves de interfaz:
```python
_UI_STRINGS = {
    "Inicio": {"en": "Home", "fr": "Accueil", "de": "Start", "pt": "Início"},
    "Se encontraron": {"en": "Found", "fr": "Trouvé(s)", "de": "Gefunden", "pt": "Encontrado(s)"},
    ...
}
```

---

### 19. NLP multilingüe — Triggers en 5 idiomas

**Teoría**: La multilingualidad también debe estar en la capa de procesamiento de lenguaje natural.

**Implementación**: `backend/nlp/intent_parser.py` — Cada set de triggers soporta 5 idiomas:

| Trigger | Líneas | Idiomas |
|---|---|---|
| `TRIGGER_ESPECIE_PERRO/GATO` | 61-67 | es, en, fr, de, pt |
| `TRIGGER_ALIMENTO` | 69-77 | es, en, fr, de |
| `TRIGGER_ACCION` | 84-106 | es, en, fr, de, pt |
| `TRIGGER_ACCESORIO` | 120-160 | es, en, fr, de, pt |
| `TRIGGER_PELAJE` | 162-171 | es, en, fr, de, pt |
| `TRIGGER_CUIDADO` | 173-246 | es, en, fr, de, pt |
| `TRIGGER_COLOR` | 248-284 | es, en, fr, de, pt |
| `TRIGGER_SEXO` | 286-292 | es, en, fr, de, pt |
| `TRIGGER_TEMPERAMENTO` | 312-346 | es, en, fr, de |
| `TRIGGER_TIPO_ALIMENTO` | 348-355 | es, en, fr, de, pt |
| `TRIGGER_FRECUENCIA` | 357-378 | es, en, fr, de, pt |
| `RAZA_MAP` (razas) | 380-415 | es, en, fr, de |

Ejemplo multilingüe en `TRIGGER_CUIDADO` (líneas 175-246):
```python
# Spanish
"baño": "Baño",
# English
"bath": "Baño",
# French
"bain": "Baño",
# German
"bad": "Baño",
# Portuguese
"banho": "Baño",
```

---

### 20. Localización — rdfs:label en Protégé (sin cambios Python)

**Teoría**: Localización de ontologías = adaptar términos a lengua y cultura local.

**Implementación**: Según `AGENTS.md` línea 58: "Adding a language = just add `rdfs:label` in Protégé, no Python changes."

Esto significa que para añadir un nuevo idioma (ej. italiano), solo se necesita:
1. Abrir `database/mascotas.rdf` en Protégé
2. Añadir `rdfs:label xml:lang="it"` a cada clase
3. Opcionalmente añadir entradas en `_UI_STRINGS`
4. Añadir triggers NLP en `intent_parser.py`

El sistema `t()` ya está preparado para leer cualquier idioma del grafo RDF.

---

### 21. Navegación y visualización con traducción

**Teoría**: La aplicación debe mostrar contenido en el idioma seleccionado.

**Implementación**: `frontend/app.py:73-86` — Menú traducido:
```python
opciones_menu = {
    "Inicio": t("Inicio", lang),
    "Perros": t("Perros", lang),
    "Gatos": t("Gatos", lang),
    "Dueños": t("Dueños", lang),
}
menu = st.segmented_control("Navigation", options=list(opciones_menu.keys()),
    format_func=lambda x: opciones_menu[x], ...)
```

`frontend/components/display.py:40-42` — Columnas traducidas:
```python
for col in df.columns:
    column_config[col] = st.column_config.TextColumn(t(col, lang))
```

---

## Esquema general del flujo teoría → implementación

```
Teoría                          Implementación
──────                          ──────────────
HTML (visualización)        →   frontend/app.py + main.css
XML (estructura)            →   database/mascotas.rdf (RDF/XML)
RDF (tripletas, grafo)      →   database/mascotas.rdf:1584-1600
RDFS (subClassOf, domain)   →   database/mascotas.rdf:26-29, 352-353, 377-378
SPARQL (consulta)           →   backend/sparql.py:82-452 (27 funciones)
URIs (recursos)             →   backend/sparql.py:44-45
OWL (ontología)             →   database/mascotas.rdf (owl:Class, owl:Property)
OWL-RL (razonador)          →   backend/sparql.py:48-55 (DeductiveClosure)
Protégé (editor)            →   database/mascotas.rdf (exportado)
rdfs:label (multilingual)   →   database/mascotas.rdf:292-395
i18n t() (traducción)       →   backend/sparql.py:506-527
Selector idioma (UI)        →   frontend/app.py:36-56
NLP multilingüe             →   backend/nlp/intent_parser.py:61-415
DBpedia (Linked Data)       →   backend/dbpedia.py:1-145
```

---

## Posibles preguntas y respuestas

### "¿Dónde está el grafo RDF?"
En `database/mascotas.rdf`. Se carga con RDFlib en `backend/sparql.py:51-52`. Cada individuo (Mascota1, Dueño47, Raza5, etc.) es un nodo del grafo.

### "¿Cómo haces consultas semánticas?"
Con SPARQL. 27 funciones en `backend/sparql.py`. Ejemplo: `get_mascotas_por_especie("Perro")` (línea 302) filtra por `:Especie2`.

### "¿Cómo funciona el razonador OWL-RL?"
`backend/sparql.py:53-54` — `DeductiveClosure(OWLRL_Semantics).expand(grafo)`. Expande el grafo con tripletas inferidas. Se aplica una vez al cargar.

### "¿Qué inferencias hace?"
Principalmente: herencia de propiedades (domain/range), clasificación por subClassOf, propiedades inversas (`tieneDueño` ↔ `tieneMacota`).

### "¿Por qué no hay restricciones OWL?"
El dominio es una base de datos de mascotas con consultas predefinidas. Las 27 consultas SPARQL cubren todas las combinaciones necesarias. Las restricciones OWL serían útiles si necesitáramos clasificación automática (ej. "si tiene 4 patas y ladra → es Perro").

### "¿Cómo implementas multilingualidad?"
Dos niveles: (1) `rdfs:label` en la ontología para nombres de clases (9 clases × 5 idiomas = 45 etiquetas), (2) `_UI_STRINGS` para textos de interfaz (~30 entradas). El selector de idioma es tipo pills en `frontend/app.py:49-56`.

### "¿Qué es DBpedia y cómo la usas?"
DBpedia es el componente de Linked Open Data del proyecto. `backend/dbpedia.py:1-145` consulta `https://es.dbpedia.org/sparql` para enriquecer resultados con origen, peso, esperanza de vida, etc. por raza.

### "¿Cómo manejas OWA?"
Las consultas SPARQL usan `OPTIONAL` para propiedades que pueden no existir (`backend/sparql.py:272-282`). No se asume nada sobre datos faltantes.

### "¿Cuál es el entrypoint?"
`main.py:1-4` → `frontend.app:main()` → `st.segmented_control` con 4 secciones.
