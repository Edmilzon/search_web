# AGENTS.md — Buscador Semántico de Mascotas

SPARQL search over RDF/OWL pet ontology (dogs, cats, breeds, owners). Streamlit app, ~4111 triples post-OWL-RL.

## Commands

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
streamlit run main.py                           # http://localhost:8501
```

## Entrypoint

`main.py` → `frontend.app:main()` → `st.segmented_control` with 4 sections. NL search + DBpedia enrichment **only** in "Inicio".

## Architecture

```
main.py                                          # entrypoint
frontend/app.py                                  # Streamlit UI + ES/EN selector
frontend/components/display.py                   # render_results(), render_results_raza() — used by app.py
frontend/components/input.py                     # ORPHANED — in __init__.py exports but never imported by app.py
frontend/styles/main.css                         # GitHub Dark theme (265 lines) — loaded via os.path.exists guard
backend/logic.py                                 # orchestrator, @lru_cache, buscar(), buscar_avanzado(), enriquecer_con_dbpedia()
backend/nlp/intent_parser.py                     # spaCy es_core_news_sm → Intent dataclass
backend/nlp/sparql_builder.py                    # Intent → intersect SPARQL results by (Nombre, Raza)
backend/sparql.py                                # 16 SPARQL query functions + cargar_ontologia() + OWL-RL reasoner
backend/dbpedia.py                               # DBpedia SPARQL via urllib + xml.etree (no external parsers)
backend/i18n.py                                  # 36 UI keys + 10 breed translations = 46 total
database/mascotas.rdf                            # RDF/XML ontology, ~2370 → ~4111 triples post-reasoning
```

No `backend/__init__.py` or `frontend/__init__.py` — only `backend/nlp/__init__.py` and `frontend/components/__init__.py` exist.

## SPARQL Essentials

- Prefix: `PREFIX : <http://www.semanticweb.org/mascotas#>`
- Species is on `Raza`, not `Mascota`: `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`
- `:Especie1` = Gato, `:Especie2` = Perro
- Query functions return `list[dict]` with columns like `"Nombre"`, `"Raza"`. Intersection in `sparql_builder.py` uses `(Nombre, Raza)` compound key.

## NL Search (spaCy)

`intent_parser.py` extracts: especie, raza, alimento, edad, dueño, sin_dueño, accesorio, pelaje.
`parse_intent()` returns `Intent` dataclass. **No intent detected** → fallback to `buscar()` (legacy keyword matching).
spaCy is singleton (`_nlp`). Model `es_core_news_sm` required.

## Reasoner

`cargar_ontologia()` applies OWL-RL (`owlrl.DeductiveClosure`) once. Global `_grafo_cache` — process-lifetime singleton.

## DBpedia

- Only `es.dbpedia.org` endpoint
- 25 breeds mapped in `_MAPA_RAZA` (26 dict entries with aliases like siames/siamés)
- Parseo: `urllib.request` + `xml.etree` only — **no TTL, no JSON, no external parsers**
- Results in separate expander in Inicio

## i18n

ES/EN selector in sidebar (`st.selectbox`). `t(texto, lang)` lookup in `TRADUCCIONES` (36 keys) + `TRADUCCIONES_RAZA` (10 keys).
