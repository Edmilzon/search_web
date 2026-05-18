# Buscador Semántico de Mascotas

Aplicación web de búsqueda semántica basada en ontología RDF para gestionar información de mascotas.

## Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                  │
│  Streamlit + Bootstrap 5 + pandas                               │
│  - Interfaz moderna con tema oscuro GitHub Dark                 │
│  - Navegación con st.segmented_control                          │
│  - Tablas interactivas con st.dataframe                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                   │
│  Python 3 + rdflib                                              │
│  - Consultas SPARQL sobre ontología                            │
│  - Lógica de búsqueda semántica con caching (@lru_cache)       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATOS                                     │
│  mascotas.rdf (RDF/XML)                                        │
│  - Ontología exportada desde Protégé                           │
│  - 110 mascotas, 52 perros, 58 gatos, 30 razas, 60 dueños     │
└─────────────────────────────────────────────────────────────────┘
```

### Tecnologías

| Capa | Tecnología | Descripción |
|------|-------------|-------------|
| **Frontend** | Streamlit | Framework web Python para UI |
| **Backend** | Python 3 | Lenguaje principal |
| **RDF** | rdflib | Librería para parsear RDF y ejecutar SPARQL |
| **Datos** | RDF/XML | Formato de ontología semántica |
| **UI** | pandas/st.dataframe | Renderizado interactivo de tablas |

### Flujo de Trabajo

```
Usuario → Streamlit (busca "Perro")
    → Python/rdflib (ejecuta SPARQL)
    → Consulta mascotas.rdf
    → Devuelve resultados
    → Streamlit (muestra tabla interactiva)
```

## Estructura del Proyecto

```
search_web/
├── main.py                    # Entry point
├── README.md                  # Este archivo
├── AGENTS.md                  # Guía para agentes IA
├── requirements.txt           # Dependencias (rdflib, streamlit, pandas)
│
├── database/
│   ├── mascotas.rdf           # Ontología RDF/XML (2370 triples)
│   └── ONTOLOGIA.md          # Documentación de la ontología
│
├── backend/
│   ├── logic.py               # Lógica principal de búsqueda (@lru_cache)
│   └── consultas/            # Módulo de consultas SPARQL
│       ├── __init__.py        # Expone 33 funciones
│       ├── base.py           # Graph() singleton + ejecutar_query()
│       ├── mascotas.py       # Consultas generales
│       ├── perros.py         # Consultas de perros
│       └── gatos.py          # Consultas de gatos
│
└── frontend/
    ├── app.py                # Aplicación Streamlit (st.segmented_control)
    ├── styles/
    │   └── main.css          # Tema oscuro GitHub Dark
    └── components/
        ├── __init__.py
        ├── display.py        # render_results() con st.dataframe
        └── input.py          # Componente de búsqueda
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
```

## Ejecución

```bash
streamlit run main.py
```

La aplicación se abrirá en: **http://localhost:8501**

## Navegación

| Sección | Descripción |
|---------|-------------|
| **Inicio** | Stats (110 mascotas, 52 perros, 58 gatos, 60 dueños) + búsqueda |
| **Perros** | Lista de perros + Información completa |
| **Gatos** | Lista de gatos + Información completa + Sin Dueño |
| **Razas** | Listado de las 30 razas |
| **Dueños** | Mascotas con sus respectivos dueños |

## Ontología

| Entidad | Cantidad | Ejemplos |
|---------|----------|----------|
| **Mascotas** | 110 | Mascota1 - Mascota110 |
| **Razas** | 30 | Labrador, Siamés, Poodle... |
| **Especies** | 2 | Perro, Gato |
| **Dueños** | 60 | Dueño1 - Dueño60 |
| **Alimentos** | 20 | Purina, Royal Canin... |
| **Accesorios** | 20 | Collar, Correa... |
| **Cuidados** | 15 | Baño, Vacunación... |

## Funcionalidades

- Búsqueda semántica por nombre de mascota
- Búsqueda por raza
- Filtrar por especie (Perro/Gato)
- Búsqueda por nombre del dueño
- Búsqueda por marca de alimento
- Ver todas las mascotas
- Ver solo perros
- Ver solo gatos
- Ver todas las razas
- Ver mascotas por dueño
- Información completa de cada mascota

## Notas

- La ontología se encuentra en `database/mascotas.rdf`
- rdflib requiere el formato RDF/XML para parsear
- Las consultas SPARQL usan el prefijo: `: <http://www.semanticweb.org/mascotas#>`
- La relación `perteneceAEspecie` está en la Raza, no en la Mascota:
  - `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`