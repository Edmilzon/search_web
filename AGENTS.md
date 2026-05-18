# AGENTS.md - Buscador Semántico de Mascotas

## Descripción

Aplicación web de búsqueda semántica basada en ontología RDF/OWL para gestionar información de mascotas (perros, gatos, razas, dueños, alimentos, accesorios y cuidados).

---

## Commands

```bash
# Install
pip install -r requirements.txt
python -m venv .venv && .venv\Scripts\activate

# Run
streamlit run main.py
# App disponible en: http://localhost:8501
```

---

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
│  mascotas.rdf (RDF/XML)                                       │
│  - Ontología exportada desde Protégé                           │
│  - 110 mascotas, 52 perros, 58 gatos, 30 razas, 60 dueños     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Trabajo

```
Usuario
   │
   ▼
┌─────────────────────────────────────────┐
│  Streamlit UI (frontend/app.py)        │
│  - Navegación: Inicio/Perros/Gatos/     │
│    Razas/Dueños                         │
│  - Búsqueda con filtros                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  backend/logic.py                      │
│  - buscar() → 5 queries secuenciales    │
│  - get_todas(), get_perros(), etc.     │
│  - @lru_cache para optimizar           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  backend/consultas/                     │
│  - SPARQL queries                       │
│  - 33 funciones de consulta             │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  backend/consultas/base.py              │
│  - cargar_ontologia() → Graph global   │
│  - ejecutar_query() → SPARQL            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  database/mascotas.rdf                 │
│  - rdflib parsea RDF/XML               │
│  - 2370 triples                         │
└─────────────────────────────────────────┘
```

---

## Navegación (st.segmented_control)

| Sección | Descripción |
|---------|-------------|
| **Inicio** | Stats (Total:110, Perros:52, Gatos:58, Dueños:60) + búsqueda |
| **Perros** | Lista de perros + Información completa |
| **Gatos** | Lista de gatos + Información completa + Sin Dueño |
| **Razas** | Listado de las 30 razas |
| **Dueños** | Mascotas con sus respectivos dueño |

---

## Arquitectura del Backend

### lógica de búsqueda (`logic.buscar()`)

```python
# 1. Busca por nombre de mascota
resultados += buscar_por_nombre_mascota(q)

# 2. Busca por raza
resultados += buscar_por_raza(q)

# 3. Busca por especie (perro/gato)
resultados += buscar_por_especie(q)

# 4. Busca por nombre del dueño
resultados += buscar_por_nombre_dueño(q)

# 5. Busca por alimento
resultados += buscar_por_alimento(q)

# 6. Deduplicar por Nombre+Raza
seen = set()
unique = [r for r in resultados if (r["Nombre"]+r["Raza"]) not in seen]
```

### Funciones con caché (`@lru_cache`)

- `get_todas()` → 110 mascotas
- `get_perros()` → 52 perros
- `get_gatos()` → 58 gatos
- `get_razas()` → 30 razas
- `get_contar_duenos()` → 60 dueñoss

### Estructura de consultas SPARQL

**Importante:** La relación `perteneceAEspecie` está en la **Raza**, no en la Mascota:
```
Mascota → tieneRaza → Raza → perteneceAEspecie → Especie
```

Ejemplo correcto:
```sparql
?mascota :tieneRaza ?raza .
?raza :perteneceAEspecie :Especie2 .  # Especie2 = Perro
```

---

## SPARQL Convention

- **Prefix:** `: <http://www.semanticweb.org/mascotas#>`
- **IRI Base:** `http://www.semanticweb.org/mascotas`
- **Propiedades (español):** `nombreMascota`, `nombreRaza`, `nombreEspecie`, `nombreDueño`, `edadMascota`, `pesoMascota`, `colorMascota`, `sexoMascota`, `esterilizado`, `tipoPelaje`

### Propiedades Objeto

| Propiedad | Dominio | Rango |
|-----------|---------|-------|
| `tieneRaza` | Mascota | Raza |
| `perteneceAEspecie` | Raza | Especie |
| `tieneDueño` | Mascota | Dueño |
| `consume` | Mascota | Alimento |
| `usa` | Mascota | Accesorio |
| `requiereCuidado` | Mascota | Cuidado |

---

## Estructura del Proyecto

```
main.py                     → Entry point (importa frontend.app:main)

frontend/
├── app.py                  → Streamlit UI (st.segmented_control)
│                           → 5 secciones: Inicio, Perros, Gatos, Razas, Dueños
├── styles/
│   └── main.css            → Tema oscuro GitHub Dark
└── components/
    ├── __init__.py         → Exports
    ├── display.py          → st.dataframe + render_results()
    └── input.py            → Search input

backend/
├── logic.py                → Orquestador con @lru_cache
│                           → buscar(), get_todas(), get_perros(), etc.
└── consultas/
    ├── __init__.py         → 33 funciones exportadas
    ├── base.py             → cargar_ontologia() + ejecutar_query()
    ├── mascotas.py         → Consultas generales
    ├── perros.py           → Consultas de perros (usa Raza.perteneceAEspecie)
    └── gatos.py            → Consultas de gatos

database/
├── mascotas.rdf            → Ontología RDF/XML (2370 triples)
└── ONTOLOGIA.md           → Documentación de la ontología
```

---

## Ontología (mascotas.rdf)

| Entidad | Cantidad | Notas |
|---------|----------|-------|
| **Mascotas** | 110 | 52 perros, 58 gatos |
| **Razas** | 30 | Labrador, Poodle, Siamés, etc. |
| **Especies** | 2 | Especie1=Gato, Especie2=Perro |
| **Dueños** | 60 | Dueño1 - Dueño60 |
| **Alimentos** | 20 | Purina, Royal Canin, etc. |
| **Accesorios** | 20 | Collar, Correa, etc. |
| **Cuidados** | 15 | Baño, Vacunación, etc. |

