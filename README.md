#  Buscador Semántico de Mascotas

Aplicación web de búsqueda semántica basada en ontología OWL para gestionar información de mascotas.

##  Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                  │
│  Streamlit (Python)                                             │
│  - Interfaz de usuario tipo "Google"                           │
│  - Tablas interactivas con pandas                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                   │
│  Python + rdflib                                                │
│  - Consultas SPARQL sobre ontología                            │
│  - Lógica de búsqueda semántica                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATOS                                     │
│  mascotas.owl (RDF/XML)                                        │
│  - Ontología OWL con Protégé                                   │
│  - 110 mascotas, 30 razas, 60 dueños                           │
└─────────────────────────────────────────────────────────────────┘
```

### Tecnologías Used

| Capa | Tecnología | Descripción |
|------|-------------|-------------|
| **Frontend** | Streamlit | Framework web Python para UI |
| **Backend** | Python 3 | Lenguaje principal |
| **RDF** | rdflib | Librería para parsear OWL y ejecutar SPARQL |
| **Datos** | OWL/RDF | Formato de ontología semántica |
| **UI** | pandas | Renderizado de tablas |

### Flujo de Trabajo

```
Usuario → Streamlit (busca "Perro")
    → Python/rdflib (ejecuta SPARQL)
    → Consulta mascotas.owl
    → Devuelve resultados
    → Streamlit (muestra tabla)
```

##  Estructura del Proyecto

```
search_web/
├── main.py                    # Entry point
├── README.md                  # Este archivo
├── AGENTS.md                  # Guía para agentes IA
├── requirements.txt           # Dependencias
│
├── database/
│   ├── mascotas.owl           # Ontología (RDF/XML)
│   ├── mascotas.owx          # Ontología (OWL/XML - Protégé)
│   └── ONTOLOGIA.md          # Documentación de la ontología
│
├── backend/
│   ├── logic.py               # Lógica principal de búsqueda
│   ├── consultas_doc.txt      # Consultas SPARQL documentadas
│   └── consultas/            # Módulo de consultas
│       ├── __init__.py
│       ├── base.py           # Conexión a ontología
│       ├── mascotas.py       # Consultas generales
│       ├── perros.py        # Consultas de perros
│       └── gatos.py          # Consultas de gatos
│
└── frontend/
    ├── app.py                # Aplicación Streamlit
    ├── components/           # Componentes UI
    │   ├── __init__.py
    │   ├── input.py          # Entrada de búsqueda
    │   └── display.py        # Renderizado de resultados
    └── pages/                # Páginas adicionales
        ├── __init__.py
        ├── mascotas.py
        ├── perros.py
        ├── gatos.py
        └── buscar.py
```

##  Instalación

### 1. Clonar el repositorio

```bash
git clone <repositorio>
cd search_web
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

##  Ejecución

```bash
streamlit run main.py
```

La aplicación se abrirá en: **http://localhost:8501**

##  Base de Datos (Ontología)

| Entidad | Cantidad | Ejemplos |
|---------|----------|----------|
| **Mascotas** | 110 | Mascota1 - Mascota110 |
| **Razas** | 30 | Labrador, Siamés, Poodle... |
| **Especies** | 2 | Perro, Gato |
| **Dueños** | 60 | Dueño1 - Dueño60 |
| **Alimentos** | 20 | Purina, Royal Canin... |
| **Accesorios** | 20 | Collar, Correa... |
| **Cuidados** | 15 | Baño, Vacunación... |

##  Consultas SPARQL

El proyecto incluye consultas predefinidas en `backend/consultas_doc.txt`:

- Buscar mascotas por nombre
- Buscar por raza
- Filtrar por especie (Perro/Gato)
- Ver mascotas porDueño
- Ver alimentos por tipo
- Ver información completa de mascotas

##  Funcionalidades

-  Búsqueda semántica por nombre de mascota
-  Búsqueda por raza
-  Filtrar por especie (Perro/Gato)
-  Búsqueda por nombre deldueño
-  Búsqueda por marca dealimento
-  Ver todas las mascotas
-  Ver solo perros
-  Ver solo gatos
-  Ver todas las razas
-  Información completade cada mascota

##  Notas

- La ontología se encuentra en `database/mascotas.owl`
- rdflib requiere el formato RDF/XML para parsear
- Las consultas SPARQL usan el prefijo: `: <http://www.semanticweb.org/mascotas#>`
