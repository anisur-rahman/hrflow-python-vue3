# HRFlow

![Backend CI](https://github.com/anisur-rahman/hrflow-python-vue3/actions/workflows/ci.yml/badge.svg)

An HR management app built with **FastAPI**, **PostgreSQL**, and **Vue 3**.

![HRFlow architecture overview](docs/images/hrflow.png)

![Dashboard](docs/images/dashboard.png)

![Add employee](docs/images/add-employee.png)

![HRFlow API](docs/images/hrflow-api.png)

## Features

- Department and employee management via REST API
- Add employees through the Vue 3 UI with form validation
- Employee directory with status tracking
- Headcount report by department
- Paginated employee list endpoint
- Swagger UI for exploring the API
- GitHub Actions CI running pytest on every push

## How data flows

1. The **Vue 3 frontend** sends HTTP requests to `/api/v1/*` via Axios
2. Vite proxies those requests to the **FastAPI backend** on port 8000
3. FastAPI validates the request using **Pydantic schemas**, then queries or writes to **PostgreSQL** via SQLAlchemy
4. The response is serialised back to JSON and returned to the frontend

### One complete example — adding John Smith

| Step | Layer | What happens |
|------|-------|--------------|
| 1 | Vue 3 | Renders the Add Employee form |
| 2 | TypeScript | Validates field types before submitting |
| 3 | Axios | POSTs employee data to `/api/v1/employees` |
| 4 | FastAPI | Validates the request with Pydantic, checks the department exists and email isn't a duplicate |
| 5 | SQLAlchemy | Inserts the employee record into PostgreSQL inside a transaction |
| 6 | FastAPI | Returns the new employee as JSON |
| 7 | Vue 3 | Refreshes the employee list automatically |
| 8 | pytest | Verifies the full create/duplicate/headcount flow in CI |
| 9 | Docker | Packages all three services together |
| 10 | GitHub Actions | Runs pytest on every push |

## Stack

| Area     | Tools                                               |
|----------|-----------------------------------------------------|
| Backend  | Python, FastAPI, SQLAlchemy 2, Pydantic v2, pytest  |
| Frontend | Vue 3 (Composition API), TypeScript, Vite, Axios    |
| Database | PostgreSQL 16 (SQLite for local dev without Docker) |
| Infra    | Docker Compose, GitHub Actions CI                   |

## Project structure

```
hrflow-python-vue3/
├── backend/
│   ├── app/
│   │   └── main.py          # FastAPI app, models, schemas, routes
│   ├── tests/
│   │   └── test_api.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.vue
│   │   │   └── Employees.vue
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css
│   ├── Dockerfile
│   └── index.html
├── docs/
│   ├── images/
│   │   ├── hrflow.png
│   │   ├── dashboard.png
│   │   ├── add-employee.png
│   │   └── hrflow-api.png
│   ├── architecture.md
│   └── deployment.md
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Getting started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git installed

### 1. Clone the repo

```bash
git clone https://github.com/anisur-rahman/hrflow-python-vue3.git
cd hrflow-python-vue3
```

### 2. Set up environment

```bash
cp .env.example .env
```

### 3. Start Docker Desktop

```bash
open -a Docker
```

Wait until Docker Desktop shows the engine is running.

### 4. Build and run

```bash
docker compose up --build
```

This starts three containers: PostgreSQL, the FastAPI backend, and the Vue 3 frontend.

### 5. Open the app

| Service | URL |
|---------|-----|
| Vue 3 frontend | http://localhost:5173 |
| FastAPI Swagger UI | http://localhost:8000/docs |

Create a department in Swagger first, then add employees through the UI.

### Troubleshooting

If the frontend doesn't load, open a second terminal and run:

```bash
docker compose ps
```

All three services (`db`, `api`, `frontend`) should show as `Up`. If one is missing, check the logs:

```bash
docker compose logs --tail=50
```

To stop the app:

```bash
docker compose down
```

## Local dev (no Docker)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Runs on SQLite locally so no database setup needed.

## Tests

```bash
cd backend
pytest -q
```

## API examples

```bash
# Create a department
curl -X POST http://localhost:8000/api/v1/departments \
  -H 'Content-Type: application/json' \
  -d '{"name":"Engineering"}'

# Add an employee
curl -X POST http://localhost:8000/api/v1/employees \
  -H 'Content-Type: application/json' \
  -d '{"name":"Jane Doe","email":"jane@example.com","department_id":1,"hire_date":"2024-03-01"}'

# Headcount by department
curl http://localhost:8000/api/v1/reports/headcount
```

## Design decisions

- SQLite is used automatically for local dev without Docker — no database setup needed
- The Vite dev server proxies all `/api/v1` requests to FastAPI, so the frontend never hardcodes a port
- Docker Compose waits for the PostgreSQL healthcheck before starting the API, preventing startup race conditions
- Pydantic v2 handles all request validation — duplicate emails and missing departments return proper 409/404 errors

## License

MIT
