# Student Management Web App

## Personal Info
- Name: [Your Name]
- Email: [Your Email]

## Tech Stack
- Backend: FastAPI
- Frontend: React
- Database: SQLite

## Tools
- Lovable
- Angrivity
- Cursor
- Windsurf

## Log
- 2026-03-07: Initialize project structure (commit: init)

## Run (backend)
1. Create a virtualenv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2. Run backend:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Run (frontend)
1. From `frontend`:

```bash
cd frontend
npm install
npm start
```

## Submission
- Commit history should show at least 2 versions: MVP and extended.
- Data files: `data/sample_students.csv` (included)

