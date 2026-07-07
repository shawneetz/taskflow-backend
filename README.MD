# TaskFlow Backend

FastAPI + PostgreSQL API for the TaskFlow task manager.

## Quick start

### GitHub Codespaces / Dev Container (recommended)

Open the repo in a Codespace or **Dev Containers: Reopen in Container**. On first launch:

1. Postgres starts on the internal `db` service
2. Dependencies install via `uv`
3. Migrations run automatically

Then start the API:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

Use **Run and Debug → FastAPI (uvicorn)** or the **Start API** task from the command palette.

### Local development (host machine)

```bash
# Start Postgres only
docker compose up -d

# Copy env and edit SECRET_KEY
cp .env.example .env

# Install deps + migrate
uv sync --extra dev
uv run alembic upgrade head

# Create test DB (once)
docker exec -it taskflow_db psql -U postgres -c "CREATE DATABASE taskflow_test;"

# Run API
uv run uvicorn app.main:app --reload --port 8000

# Tests
uv run pytest -v
```

## Self-hosted production

Production stack (db + backend + Cloudflare Tunnel) lives in [`docker/`](docker/):

```bash
cd docker
cp .env.example .env   # fill in secrets
docker compose up -d --build
```

**Monorepo layout** (`taskflow/docker/` + `taskflow/backend/`): copy the `docker/` folder to your project root and set `build: ../backend` in `docker-compose.yaml`.

Point your Cloudflare Tunnel public hostname at `http://backend:8000`.

## Environment variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | Postgres URL (`postgresql://` auto-normalized to `+asyncpg`) |
| `SECRET_KEY` | JWT signing key (64-char hex in production) |
| `CORS_ORIGINS` | Comma-separated frontend origin(s) |
| `TEST_DATABASE_URL` | Test DB URL (Codespace uses `@db`, local uses `@localhost`) |
| `DEBUG` | SQL echo + dev behavior |

See [`.env.example`](.env.example) for local dev and [`docker/.env.example`](docker/.env.example) for production.

## Project layout

```
app/           # FastAPI application
alembic/       # Database migrations
tests/         # Pytest suite
scripts/       # Container entrypoint
docker/        # Production compose + env template
.devcontainer/ # Codespace / Dev Container config
```
