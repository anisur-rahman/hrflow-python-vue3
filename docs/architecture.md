# Architecture

```
Vue 3 (Vite)  →  FastAPI  →  PostgreSQL
   :5173           :8000
```

The frontend proxies all `/api/v1` requests to the FastAPI backend via Vite's dev server proxy (or the `frontend` Docker service in Compose). FastAPI connects to PostgreSQL using SQLAlchemy 2 with mapped column syntax. SQLite is used automatically when no `DATABASE_URL` env var is set, which keeps local dev simple.

Everything runs as three Docker Compose services: `db`, `api`, and `frontend`. The API waits for the database healthcheck before starting.
