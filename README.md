# GridGuard AI — Stage 1

A local energy data foundation and dashboard for generation companies and distribution utilities. **Every included value is synthetic demonstration data**, not a report of real companies or operating measurements.

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is at `http://127.0.0.1:8000`; interactive docs are at `/docs`. SQLite is created as `backend/gridguard.db` and seeded on first startup.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Vite serves the dashboard at `http://localhost:5173`. Set `VITE_API_URL` to change the API origin (default `http://127.0.0.1:8000`).

## GitHub Pages hosting

The React dashboard is configured for GitHub Pages at `https://balaji08953.github.io/MINI_PROJECT_AMGRCET/`. The Actions workflow builds and deploys it after pushes to `main`. In repository settings, choose **Pages → Build and deployment → Source → GitHub Actions** if needed. The published dashboard shows labeled synthetic demo values without a backend. GitHub Pages hosts static files only; to connect API readings, host `backend/` on a Python service and add an Actions repository variable named `VITE_API_URL` containing its API base URL. Configure that service’s CORS allowlist to include the Pages origin.

## Structure and data model

- `backend/app/models.py`: SQLAlchemy entities and relationships.
- `backend/app/seed.py`: repeatable synthetic demo records (companies, plants, utilities, substations, feeders and transformers).
- `backend/app/main.py`: FastAPI app and read endpoints.
- `frontend/src/`: React dashboard, charts and searchable tables.

Generation companies own plants; each plant stores its generation type, renewable classification, capacity, current MW output, daily MWh, availability, status and timestamp. Utilities own substations, which own feeders, which own distribution transformers. Utility readings store demand, received and supplied MW, estimated losses in MW and percent, outage count and timestamp. All power uses MW; energy uses MWh. The current API exposes `/api/overview`, `/api/generation/companies`, `/api/generation/plants`, `/api/utilities`, `/api/substations`, `/api/feeders`, and `/api/transformers`.

The schema separates entities from readings/assets so verified datasets can replace the sample records as the project grows. No forecasting, control, or fault-detection functions are included.
