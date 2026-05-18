# AGENTS.md

Semantic web search app using RDF/OWL ontology with Streamlit UI.

## Commands

```bash
# Install
pip install -r requirements.txt
python -m venv .venv && .venv\Scripts\activate

# Run (NOT python main.py)
streamlit run main.py
```

## Key Architecture

- **Entry chain**: `main.py` → imports → `frontend/app.py:main()` (NOT `app.py` directly)
- **Backend layers**: `logic.py` (search orchestration) → `consultas/` (SPARQL execution)
- **Search pattern**: `logic.buscar()` runs 5 sequential queries (nombre→raza→especie→dueño→alimento) then deduplicates by `Nombre+Raza`
- **Frontend**: Single-page Streamlit app with internal navigation (radio button switches views), not multi-page, uses Bootstrap 5 + custom CSS
- **Ontology**: Globally cached in `backend/consultas/base.py:cargar_ontologia()` (rdflib Graph cached globally)

## SPARQL Convention

- Prefix: `: <http://www.semanticweb.org/mascotas#>`
- Properties use full Spanish names: `nombreMascota`, `nombreRaza`, `nombreEspecie`, `nombreDueño`, `nombreAlimento`
- Ontology format: RDF/XML at `database/mascotas.owl`

## Project Structure

```
main.py                 → Entry point
frontend/app.py         → Streamlit UI (single-page, radio nav)
frontend/components/
├── input.py            → Search input component
├── display.py          → Results rendering (pandas tables)
└── search.py           → Search utilities
frontend/pages/         → UNUSED (dead code, not integrated)
backend/logic.py        → Search orchestration
backend/consultas/
├── base.py            → Graph() singleton + ejecutar_query()
├── __init__.py        → Exports 33 query functions
├── mascotas.py        → General queries
├── perros.py          → Dog-specific queries
└── gatos.py           → Cat-specific queries
database/mascotas.owl → OWL ontology RDF/XML (110 pets, 30 breeds, 60 owners)
```

## Notes

- No test framework configured
- No lint/typecheck configured