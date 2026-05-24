# AGENTS.md - Buscador Semántico de Mascotas

Búsqueda semántica vía SPARQL sobre ontología RDF/OWL de mascotas (perros, gatos, razas, dueños).

## Commands

```bash
pip install -r requirements.txt               # rdflib, streamlit, pandas, spacy, owlrl
python -m spacy download es_core_news_sm       # modelo spaCy español (post-install)
streamlit run main.py                          # http://localhost:8501
```

## Entrypoint

`main.py` → `frontend.app:main()` → `st.segmented_control` (6 secciones: Inicio, Perros, Gatos, Razas, Dueños, Búsqueda Avanzada)

## Architecture

```
frontend/app.py                  # Streamlit UI + Bootstrap 5 dark theme + selector idioma
frontend/components/             # display.py, input.py
backend/logic.py                 # Orquestador, @lru_cache, buscar_avanzado(), enriquecer_con_dbpedia()
backend/nlp/                     # NL → SPARQL: intent_parser.py (spaCy) + sparql_builder.py
backend/i18n.py                  # Traducciones ES/EN
backend/consultas/               # SPARQL (31 funciones exportadas)
  ├── base.py                    # cargar_ontologia() + razonador OWL-RL (owlrl)
  ├── dbpedia.py                 # Consultas a DBpedia vía SPARQL endpoint XML
  ├── mascotas.py, perros.py, gatos.py
database/mascotas.rdf            # Ontología RDF/XML, 4111 triples post-razonamiento
```

## Quick Quirks

- **SPARQL:** `perteneceAEspecie` está en `Raza`, no en `Mascota`. Ruta: `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`. `:Especie1` = Gato, `:Especie2` = Perro
- **Búsqueda Avanzada (NL):** Usa spaCy (`es_core_news_sm`) para parsear oraciones completas. `backend/nlp/intent_parser.py` extrae intenciones (especie, raza, alimento, edad, dueño, sin_dueño) y `sparql_builder.py` intersecta resultados combinando múltiples filtros
- **OWL Reasoner:** `cargar_ontologia()` aplica razonamiento OWL-RL (vía `owlrl`) en primera carga, expandiendo triples de ~2370 a ~4111
- **DBpedia:** `backend/consultas/dbpedia.py` consulta endpoint SPARQL de DBpedia, parsea XML nativo (sin JSON/TTL/parsers externos). Se muestra en expander separado en Búsqueda Avanzada
- **i18n:** Selector ES/EN en sidebar. Traducciones en `backend/i18n.py` para UI y resultados
- **Graph singleton:** `cargar_ontologia()` cachea en `_grafo_cache` global
- **No hay tests** — sin pytest, CI, o fixtures
- **No hay linter/formatter/typecheck** configurados
