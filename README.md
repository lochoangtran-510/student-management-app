# Student Management (Vibe Coding)

Personal: Tran Hoang Xuan Loc

Tech stack: FastAPI, React-like simple frontend (HTML+JS), SQLite

Tools: Lovable, Angrivity, Cursor, Windsurf…

Log:

- Phase 1 (MVP): scaffolded FastAPI backend and a simple frontend UI. Implemented add/list/edit/delete, search, export, stats endpoint. Created seed data.
- Phase 2 planned: add Class table, assign students to classes, add per-class listing, improved React frontend.

Run (backend):

1. Create a virtualenv and install dependencies

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

2. Start the API server

```bash
uvicorn backend.app.main:app --reload --factory
```

3. (Optional) Seed example data

```bash
python backend/seed.py
```

Open the frontend: open `frontend/index.html` in a browser (or serve it with a static server). The frontend expects the API at `http://localhost:8000`.

Deliverables:

- `backend/` — FastAPI app
- `frontend/` — simple UI
- `backend/seed_data.csv` — sample data
- README.md
