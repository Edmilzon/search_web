# AGENTS.md - Buscador Semántico de Mascotas

Búsqueda semántica vía SPARQL sobre ontología RDF/OWL de mascotas (perros, gatos, razas, dueños).  
Streamlit app, Python 3, ~4111 triples post-razonamiento OWL-RL.

## Commands

```bash
pip install -r requirements.txt               # rdflib, streamlit, pandas, spacy, owlrl
python -m spacy download es_core_news_sm       # modelo spaCy español (post-install)
streamlit run main.py                          # http://localhost:8501
```

## Entrypoint

`main.py` → `frontend.app:main()` → `st.segmented_control` (4 secciones: Inicio, Perros, Gatos, Razas).  
Búsqueda avanzada NL + DBpedia están en la página **Inicio**, no son secciones aparte.

## Architecture

```
frontend/app.py                  # Streamlit UI + Bootstrap 5 dark theme + selector idioma
frontend/components/             # display.py, input.py
backend/logic.py                 # Orquestador, @lru_cache, buscar_avanzado(), enriquecer_con_dbpedia()
backend/nlp/                     # NL → SPARQL: intent_parser.py (spaCy) + sparql_builder.py
backend/i18n.py                  # Traducciones ES/EN (~48 claves)
backend/sparql.py                # 20 funciones SPARQL + cargar_ontologia() + razonador OWL-RL (owlrl)
backend/dbpedia.py               # Consultas a DBpedia vía SPARQL endpoint, parseo XML nativo (xml.etree)
database/mascotas.rdf            # Ontología RDF/XML, ~2370 → ~4111 triples post-razonamiento
```

## Quick Quirks

- **SPARQL:** `perteneceAEspecie` está en `Raza`, no en `Mascota`. Ruta: `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`. `:Especie1` = Gato, `:Especie2` = Perro
- **NL search:** spaCy (`es_core_news_sm`) extrae intenciones (especie, raza, alimento, edad, dueño, sin_dueño, accesorio, pelaje). `sparql_builder.py` intersecta resultados combinando múltiples filtros. Si no detecta intención → fallback a `buscar()` (legacy keyword)
- **Reasoner:** `cargar_ontologia()` aplica OWL-RL (owlrl) en primera carga. Cachea global en `_grafo_cache`
- **DBpedia:** Solo español (`es.dbpedia.org`). 26 razas mapeadas. Parseo XML nativo sin librerías externas. Resultados en expander separado en Inicio
- **Constraints (Correcciones.txt):** NO usar TTL, NO usar parsers externos, NO usar JSON — todo SPARQL + XML nativo (`xml.etree`) o rdflib
- **i18n:** Selector ES/EN en sidebar. Traducciones en `backend/i18n.py` para UI y resultados
- **No tests** — sin pytest, CI, o fixtures
- **No linter/formatter/typecheck** configurados
