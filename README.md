# Buscador Semántico de Mascotas

Aplicación web de búsqueda semántica vía SPARQL sobre ontología RDF/OWL de mascotas (perros, gatos, razas, dueños).  
Soporta búsqueda en lenguaje natural, razonamiento OWL, enriquecimiento con DBpedia e internacionalización ES/EN.

## Stack Tecnológico

```
┌────────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                    │
│  Streamlit + Bootstrap 5 + pandas + CSS personalizado              │
│  - Navegación con st.segmented_control (pills)                    │
│  - Tema oscuro GitHub Dark                                         │
│  - Tablas interactivas con st.dataframe                            │
│  - Selector de idioma ES/EN integrado                              │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                      BACKEND (Python 3)                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  NLP spaCy  │  │  SPARQL      │  │  i18n        │              │
│  │  Intent     │  │  rdflib +    │  │  48         │              │
│  │  Parser     │  │  OWL-RL      │  │  traducciones│              │
│  │  + Builder  │  │  @lru_cache  │  │  ES/EN       │              │
│  └─────────────┘  └──────────────┘  └──────────────┘              │
│  ┌──────────────────────────────────────────────┐                  │
│  │  DBpedia (SPARQL endpoint vía HTTP XML)       │                 │
│  │  Enriquecimiento: origen, peso, esperanza de  │                 │
│  │  vida de 26 razas mapeadas                    │                 │
│  └──────────────────────────────────────────────┘                  │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                         DATOS                                       │
│  database/mascotas.rdf (RDF/XML)                                   │
│  - Ontología exportada desde Protégé                               │
│  - 110 mascotas, 52 perros, 58 gatos, 30 razas, 60 dueños         │
│  - 4111 triples post-razonamiento OWL-RL                           │
└────────────────────────────────────────────────────────────────────┘
```

### Tecnologías

| Capa | Tecnología | Descripción |
|------|------------|-------------|
| **Frontend** | Streamlit 1.40+ | Framework web Python para UI |
| **Backend** | Python 3 | Lenguaje principal |
| **RDF/OWL** | rdflib 7.1+ | Parseo RDF y ejecución SPARQL |
| **Razonador** | owlrl 7.1+ | Razonamiento OWL-RL (~2370 → 4111 triples) |
| **NLP** | spaCy + es_core_news_sm | Parsing de lenguaje natural, extracción de intenciones |
| **DBpedia** | SPARQL endpoint + XML nativo | Enriquecimiento de razas |
| **i18n** | backend/i18n.py | 48 traducciones ES/EN (± 82 strings de UI) |
| **UI** | pandas/st.dataframe | Renderizado interactivo de tablas |
| **Caching** | functools.lru_cache | Resultados SPARQL cacheados en memoria |

### Flujo de Trabajo

```
Usuario → "perros que comen Purina"
    → spaCy (intent_parser.py → especie=Perro + alimento=Purina)
    → sparql_builder.py (intersecta resultados de ambas consultas)
    → rdflib (ejecuta SPARQL contra mascotas.rdf)
    → Enriquecimiento DBpedia (en expander separado)
    → Streamlit (tabla interactiva con resultados)
```

### Búsqueda Avanzada (NL)

| Patrón | Ejemplo | Intersección |
|--------|---------|--------------|
| Especie + raza | `gato persa` | Gatos + raza Persa |
| Especie + alimento | `perro que come purina` | Perros + Purina |
| Dueño | `mascotas de Carlos` / `dueño Carlos` | Filtro por dueño |
| Edad | `3 años` / `mascotas de 5 años` | Filtro por edad |
| Accesorio | `gato con collar` | Gatos + Collar |
| Pelaje | `pelaje corto` | Filtro por tipo de pelaje |
| Sin dueño | `sin dueño` | Mascotas sin dueño registrado |
| Simple keyword | `akita` (caída a legacy `buscar()`) | Búsqueda por nombre/raza |

## Estructura del Proyecto

```
search_web/
├── main.py                         # Entry point → frontend.app.main()
├── README.md                       # Este archivo
├── AGENTS.md                       # Guía para agentes IA
├── requirements.txt                # rdflib, streamlit, pandas, spacy, owlrl
├── .gitignore
│
├── database/
│   └── mascotas.rdf               # Ontología RDF/XML (4111 triples post-razonamiento)
│
├── backend/
│   ├── __init__.py
│   ├── logic.py                   # Orquestador, @lru_cache, buscar/buscar_avanzado
│   ├── sparql.py                  # 18 funciones SPARQL + cargar_ontologia + OWL-RL
│   ├── dbpedia.py                 # Consultas DBpedia vía SPARQL endpoint HTTP/XML
│   ├── i18n.py                    # 48 traducciones ES/EN
│   └── nlp/
│       ├── __init__.py
│       ├── intent_parser.py       # spaCy → Intent (especie, raza, alimento, edad, ...)
│       └── sparql_builder.py      # Intent → intersección de resultados SPARQL
│
├── frontend/
│   ├── __init__.py
│   ├── app.py                    # Streamlit UI: navbar, pills, buscador centrado
│   └── components/
│       ├── __init__.py
│       └── display.py            # render_results(), render_results_raza()
│
└── styles/
    └── main.css                  # Tema oscuro GitHub Dark
```

## Instalación

```bash
# Clonar y entrar al directorio
cd search_web

# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo spaCy español
python -m spacy download es_core_news_sm
```

## Ejecución

```bash
streamlit run main.py
```

La aplicación se abrirá en: **http://localhost:8501**

## Navegación

| Sección | Descripción |
|---------|-------------|
| **Inicio** | Stats (110 mascotas, 52 perros, 58 gatos, 60 dueños) + búsqueda inteligente centrada |
| **Perros** | Lista de perros con información completa |
| **Gatos** | Lista de gatos con información completa |
| **Razas** | Listado de las 30 razas |
| **Dueños** | Mascotas con sus respectivos dueños |

## Funcionalidades

- Búsqueda en **lenguaje natural** (spaCy): `"mostrar gatos persa que comen purina"`
- Búsqueda simple por keyword (caída automática a legacy)
- Intersección de múltiples filtros (especie + raza + alimento + edad + ...)
- Razonamiento **OWL-RL** en carga inicial (~2370 → 4111 triples)
- Enriquecimiento **DBpedia** para 26 razas (origen, peso, esperanza de vida)
- **Internacionalización ES/EN** (48 traducciones, selector en UI)
- Tema oscuro **GitHub Dark**
- Cacheo de resultados SPARQL con `@lru_cache`
- Sin dependencias externas de parsing DBpedia (XML nativo vía `xml.etree`)

## Ontología

La ontología se encuentra en `database/mascotas.rdf` y contiene:

| Entidad | Cantidad | Ejemplos |
|---------|----------|----------|
| **Mascotas** | 110 | Mascota1 – Mascota110 |
| **Razas** | 30 | Labrador, Siamés, Poodle, Persa… |
| **Especies** | 2 | Perro, Gato |
| **Dueños** | 60 | Dueño1 – Dueño60 |
| **Alimentos** | 20 | Purina, Royal Canin, Whiskas… |
| **Accesorios** | 20 | Collar, Correa, Juguete… |
| **Cuidados** | 15 | Baño, Vacunación… |

Prefijo SPARQL: `: <http://www.semanticweb.org/mascotas#>`

### Relaciones clave

- `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`  
  La especie se determina a través de la raza, no directamente en `Mascota`.
- `:Especie1` = Gato, `:Especie2` = Perro

## Notas

- **Razonamiento OWL**: Se aplica automáticamente en la primera carga (vía `owlrl`), expandiendo triples.
- **Graph singleton**: `cargar_ontologia()` cachea el grafo en `_grafo_cache` global.
- **DBpedia**: Las consultas se hacen al endpoint SPARQL público de DBpedia. Los resultados se muestran en un expander separado en la sección de búsqueda. Sin mapeo TTL/JSON — parseo XML nativo.
