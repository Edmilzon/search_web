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
│  │  Intent     │  │  rdflib +    │  │  47          │              │
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
| **i18n** | backend/i18n.py | 47 traducciones ES/EN |
| **UI** | pandas/st.dataframe | Renderizado interactivo de tablas |
| **Caching** | functools.lru_cache | Resultados SPARQL cacheados en memoria |

### Flujo de Trabajo

```
Usuario → "mostrar gatos persa de color blanco que comen purina"
    → spaCy (intent_parser.py → especie=Gato + raza=Persa + color=Blanco + alimento=Purina)
    → sparql_builder.py (intersecta resultados de TODAS las consultas)
    → rdflib (ejecuta SPARQL contra mascotas.rdf)
    → Enriquecimiento DBpedia (en expander separado)
    → Streamlit (tabla interactiva con resultados)
```

---

## Búsqueda Inteligente (NL)

El buscador entiende **lenguaje natural** usando spaCy. Detecta automáticamente 15+ propiedades de la ontología y las combina en una **intersección múltiple** (AND lógico). Si no se detecta ninguna intención, cae automáticamente a búsqueda por keyword (nombre + raza).

### Propiedades detectables

| Propiedad | Ontología | Ejemplos |
|-----------|-----------|----------|
| **especie** | `perteneceAEspecie` | `perro`, `gato`, `perra`, `gata`, `can`, `felino` |
| **raza** | `nombreRaza` | `labrador`, `persa`, `poodle`, `siamés`, `bulldog` |
| **color** | `colorMascota` | `blanco`, `negro`, `marrón`, `gris`, `dorado`, `chocolate` |
| **sexo** | `sexoMascota` | `macho`, `hembra`, `masculino`, `femenino` |
| **edad** | `edadMascota` | `3 años`, `edad 5`, `5 años` |
| **peso** | `pesoMascota` | `5 kg`, `10 kilos` |
| **pelaje** | `tipoPelaje` | `corto`, `largo`, `rizado`, `liso` |
| **alimento** (marca) | `marcaAlimento` | `Royal`, `Purina`, `Whiskas` |
| **tipo alimento** | `tipoAlimento` | `seco`, `húmedo` |
| **accesorio** | `nombreAccesorio` | `collar`, `correa`, `juguete` |
| **dueño** | `nombreDueño` | `dueño Carlos`, `mascotas de María` |
| **sin dueño** | `tieneDueño` (negación) | `sin dueño`, `sin dueña` |
| **esterilizado** | `esterilizado` | `esterilizado`, `castrado`, `sin esterilizar` |
| **bozal** | `requiereBozal` | `con bozal`, `sin bozal` |
| **temperamento** | `temperamento` (Raza) | `tranquilo`, `juguetón`, `activo`, `dócil` |
| **cuidado** | `tipoCuidado` | `baño`, `vacunación`, `veterinario` |
| **frecuencia cuidado** | `frecuenciaCuidado` | `semanal`, `mensual` |
| **acción** | (meta) | `listar`, `mostrar`, `dame`, `cuántos` |

### Ejemplos de búsquedas complejas

| Búsqueda | Qué detecta | Explicación |
|----------|-------------|-------------|
| `gato blanco` | especie=Gato + color=Blanco | Gatos de color blanco |
| `perro marrón de 3 años` | especie=Perro + color=Marrón + edad=3 | Perros marrones de 3 años |
| `gato hembra esterilizado` | especie=Gato + sexo=Hembra + esterilizado=True | Gatas esterilizadas |
| `perro macho sin bozal` | especie=Perro + sexo=Macho + bozal=False | Perros machos que NO requieren bozal |
| `perro que come alimento seco` | especie=Perro + tipo_alimento=Seco | Perros que comen alimento seco |
| `gato tranquilo` | especie=Gato + temperamento=Tranquilo | Gatos de raza tranquila |
| `gato que necesita baño` | especie=Gato + cuidado=Baño | Gatos que requieren baño |
| `perro que come Royal` | especie=Perro + alimento=Royal | Perros que comen Royal Canin |
| `listar gatos persa con collar` | accion=listar + especie=Gato + raza=Persa + accesorio=Collar | Lista gatos Persa que usan collar |
| `cuántos perros sin dueño` | accion=contar + especie=Perro + sin_dueño=True | Cuenta perros sin dueño |
| `dame perros de Carlos` | accion=listar + especie=Perro + dueño=Carlos | Perros cuyo dueño es Carlos |
| `mostrar gatos de color blanco que comen purina` | accion=listar + especie=Gato + color=Blanco + alimento=Purina | Gatos blancos que comen Purina |
| `perro pelaje corto de 5 años` | especie=Perro + pelaje=Corto + edad=5 | Perros de pelo corto de 5 años |
| `gato de 4 kilos` | especie=Gato + peso=4 | Gatos que pesan 4 kg |
| `gato sin esterilizar` | especie=Gato + esterilizado=False | Gatos no esterilizados |
| `perro con collar y correa` | especie=Perro + accesorio=Collar | Perros con collar (único accesorio detectado) |

> **Nota:** Cuando se combinan múltiples criterios, todos se intersecan (AND). Por ejemplo, `gato blanco macho de 3 años` busca gatos que sean **simultáneamente** blancos, machos y de 3 años.

### Caída a búsqueda simple

Si ninguna intención es detectada (ej: `"akita"`, `"Bobby"`), el sistema cae automáticamente a `buscar()` que busca por keyword en nombre de mascota, raza, especie, dueño y alimento.

---

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
│   ├── logic.py                   # Orquestador, @lru_cache, buscar/buscar_avanzado
│   ├── sparql.py                  # 18 funciones SPARQL + cargar_ontologia + OWL-RL
│   ├── dbpedia.py                 # Consultas DBpedia vía SPARQL endpoint HTTP/XML
│   ├── i18n.py                    # 47 traducciones ES/EN
│   └── nlp/
│       ├── intent_parser.py       # spaCy → Intent (especie, raza, alimento, color, ...)
│       └── sparql_builder.py      # Intent → intersección de resultados SPARQL
│
├── frontend/
│   ├── app.py                    # Streamlit UI: navbar, pills, buscador centrado
│   └── components/
│       ├── __init__.py
│       └── display.py            # render_results(), clasificar_tipo()
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
| **Inicio** | Stats (110 mascotas, 52 perros, 58 gatos, 19 dueños) + búsqueda inteligente centrada |
| **Perros** | 52 perros agrupados por raza en expanders, con info completa (edad, peso, color, dueño, alimento) |
| **Gatos** | 58 gatos agrupados por raza en expanders, con info completa |
| **Dueños** | 19 dueños únicos, cada uno en un expander con sus mascotas y tipo (Perro/Gato) |

## Funcionalidades

- Búsqueda en **lenguaje natural** (spaCy): reconoce 15+ propiedades de la ontología
- Intersección **AND** de múltiples filtros: cualquier combinación de especie + raza + color + sexo + edad + peso + alimento + ...
- Razonamiento **OWL-RL** en carga inicial (~2370 → 4111 triples)
- Enriquecimiento **DBpedia** para 26 razas (origen, peso, esperanza de vida)
- **Internacionalización ES/EN** (47 traducciones, selector en UI)
- Tema oscuro **GitHub Dark**
- Cacheo de resultados SPARQL con `@lru_cache`
- Sin dependencias externas de parsing DBpedia (XML nativo vía `xml.etree`)
- Expansión por raza en secciones Perros y Gatos
- Agrupación por dueño con tipo de mascota (🐕/🐈) en sección Dueños

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
- `colorMascota`, `sexoMascota`, `edadMascota`, `pesoMascota`, `tipoPelaje`, `esterilizado`, `requiereBozal` son propiedades directas de `Mascota`
- `temperamento` es propiedad de `Raza`
- `tipoAlimento` es propiedad de `Alimento`
- `tipoCuidado` y `frecuenciaCuidado` son propiedades de `Cuidado`

## Notas

- **Razonamiento OWL**: Se aplica automáticamente en la primera carga (vía `owlrl`), expandiendo triples.
- **Graph singleton**: `cargar_ontologia()` cachea el grafo en `_grafo_cache` global.
- **DBpedia**: Las consultas se hacen al endpoint SPARQL público de DBpedia. Los resultados se muestran en un expander separado en la sección de búsqueda. Sin mapeo TTL/JSON — parseo XML nativo.
- **Columna Tipo**: La función `clasificar_tipo(raza)` asigna 🐕 Perro o 🐈 Gato según listas de razas conocidas, usada en tablas de resultados y sección Dueños.
