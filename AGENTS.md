# AGENTS.md

## Project Overview

Semantic web search application using RDF/OWL ontology with a Streamlit web interface.

## Tech Stack

| Capa | Tecnología |
|------|------------|
| Frontend | Streamlit + pandas |
| Backend | Python + rdflib |
| Datos | OWL ontology (RDF/XML) |

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Run the app
streamlit run main.py
```

## Project Structure

```
search_web/
├── main.py                    # Entry point (NOT app.py)
├── database/
│   └── mascotas.owl          # Ontology (RDF/XML)
├── backend/
│   ├── logic.py             # Main search logic
│   └── consultas/           # SPARQL queries by category
│       ├── base.py          # Ontology connection
│       ├── mascotas.py      # General queries
│       ├── perros.py       # Dog-specific queries
│       └── gatos.py        # Cat-specific queries
└── frontend/
    ├── app.py              # Main Streamlit app
    ├── components/         # UI components
    │   ├── input.py        # Search input
    │   └── display.py     # Table rendering
    └── pages/              # Additional pages
```

## Development Notes

- Entry point is `main.py`, NOT `app.py`
- Ontology at `database/mascotas.owl` (RDF/XML format)
- SPARQL prefix: `: <http://www.semanticweb.org/mascotas#>`
- Properties use full names: `nombreMascota`, `nombreRaza`, `nombreEspecie`
- Ontology cached globally in `backend/consultas/base.py`
- Run with `streamlit run main.py` (NOT `python main.py`)