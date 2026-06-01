# AGENTS.md — Buscador Semántico de Mascotas

SPARQL search over RDF/OWL pet ontology (dogs, cats, breeds, owners). Streamlit app, ~4111 triples post-OWL-RL.

## Commands

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
streamlit run main.py                           # http://localhost:8501
```

No test/lint/typecheck commands exist. `.gitignore` excludes `AGENTS.md` — use `git add -f AGENTS.md` to commit changes.

## Entrypoint

`main.py` → `frontend.app:main()` → `st.segmented_control` with 4 sections. NL search + DBpedia enrichment **only** in "Inicio".

## Import Quirk

`frontend/app.py:5` does `sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))` — the app runs as **script only** (`streamlit run main.py`), never as `python -m`. There are no `backend/__init__.py` or `frontend/__init__.py` files (only `backend/nlp/__init__.py` and `frontend/components/__init__.py` exist).

## Architecture

```
main.py                                          # entrypoint (4 lines)
frontend/app.py                                  # Streamlit UI + ES/EN selector in columns (not sidebar)
frontend/components/display.py                   # render_results(), clasificar_tipo() — used by app.py
frontend/components/input.py                     # ORPHANED — exported from __init__.py but never imported by app.py
frontend/styles/main.css                         # GitHub Dark theme — loaded via os.path.exists guard
backend/logic.py                                 # orchestrator, buscar(), buscar_avanzado(), enriquecer_con_dbpedia()
backend/logic.py                                 # @lru_cache on: get_todas, get_perros, get_gatos, get_todos_duenos, info_perros, info_gatos
backend/nlp/intent_parser.py                     # spaCy es_core_news_sm → Intent dataclass
backend/nlp/sparql_builder.py                    # Intent → intersect SPARQL results by (Nombre, Raza) compound key
backend/sparql.py                                # 21 SPARQL query functions + cargar_ontologia() + OWL-RL reasoner + t() i18n (RDF-backed)
backend/dbpedia.py                               # DBpedia SPARQL via urllib + xml.etree (no external parsers, no rdflib)
database/mascotas.rdf                            # RDF/XML ontology, ~2370 → ~4111 triples post-reasoning
```

## SPARQL Essentials

- Prefix: `PREFIX : <http://www.semanticweb.org/mascotas#>`
- Species is on `Raza`, not `Mascota`: `Mascota → tieneRaza → Raza → perteneceAEspecie → Especie`
- `:Especie1` = Gato, `:Especie2` = Perro. In `sparql.py:283` both species are hardcoded — update both places if adding a new species.
- Query functions return `list[dict]`. Intersection in `sparql_builder.py` uses `(Nombre, Raza)` compound key.
- `_sanitizar()` in `sparql.py:7` strips `"` and `\` from user input before SPARQL injection — use for any new query functions that embed user input.

## NL Search (spaCy)

`intent_parser.py` extracts: especie, raza, color, sexo, edad, peso, pelaje, alimento, tipo_alimento, accesorio, dueño, sin_dueño, esterilizado, requiere_bozal, temperamento, cuidado, frecuencia_cuidado.
`parse_intent()` returns `Intent` dataclass. **No intent detected** → fallback to `buscar()` (legacy keyword matching).
spaCy is singleton (`_nlp`). Model `es_core_news_sm` required.

## Reasoner

`cargar_ontologia()` applies OWL-RL (`owlrl.DeductiveClosure`) once. Global `_grafo_cache` — process-lifetime singleton. Ontology path is relative: `os.path.join(__file__, "..", "..", "database", "mascotas.rdf")`.

## DBpedia

- Only `es.dbpedia.org` endpoint (hardcoded in `dbpedia.py:6`)
- 29 entries in `_MAPA_RAZA` (26 breeds + aliases like siames/siamés)
- Parsing: `urllib.request` + `xml.etree` only — **no TTL, no JSON, no external parsers**
- Requires `User-Agent: Mozilla/5.0` header in requests
- Results shown in separate expander in Inicio

## i18n

5-language selector (es, en, fr, de, pt) in column layout (`st.columns`, not sidebar). `t(texto, lang)` lives in `backend/sparql.py` — reads `rdfs:label` from the RDF graph for 9 class names (Perro, Gato, Raza, Dueño, Mascota, Especie, Accesorio, Alimento, Cuidado), falls back to a `_UI_STRINGS` dict (~30 entries) for UI-only keys. Adding a language = just add `rdfs:label` in Protégé, no Python changes.
