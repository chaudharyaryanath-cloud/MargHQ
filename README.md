# MargHQ

Career exploration and planning in one small web app. Take the work-style quiz to explore career directions, or enter a target job to get a 12-week workflow.

## Run locally

From the project root in PowerShell:

```powershell
.\backend\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload --port 8000
```

Open `http://localhost:8000/`. The API docs are at `http://localhost:8000/docs`.

## Endpoints

- `POST /api/assess` scores the work-style quiz and suggests starter projects.
- `POST /api/find-career` matches interests, strengths, personality, and work style.
- `POST /generate-roadmap` accepts `{ "targetJob": "UX Designer" }` and returns workflow nodes and edges.
- `GET /health` checks server status.

The frontend is served by FastAPI, so its forms call the API on the same origin.
