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
- **Search pattern**: `logic.buscar()` runs 5 parallel queries then deduplicates by `Nombre+Raza`
- **Ontology**: Globally cached in `backend/consultas/base.py:cargar_ontologia()`

## SPARQL Convention

- Prefix: `: <http://www.semanticweb.org/mascotas#>`
- Properties use full Spanish names: `nombreMascota`, `nombreRaza`, `nombreEspecie`, `nombreDueño`, `nombreAlimento`
- Ontology format: RDF/XML at `database/mascotas.owl`

## Project Structure

```
main.py                 → Entry point
frontend/app.py         → Streamlit UI (pages: inicio, perros, gatos, búsqueda, razas)
backend/logic.py        → Search orchestration
backend/consultas/
├── base.py            → Graph() singleton + ejecutar_query()
├── mascotas.py        → General queries
├── perros.py          → Dog-specific
└── gatos.py           → Cat-specific
database/mascotas.owl  → OWL ontology (110 pets, 30 breeds, 60 owners)
```

## Notes

- No test framework configured
- No lint/typecheck configured