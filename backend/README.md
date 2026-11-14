# Identity Chain API

FastAPI backend using PostgreSQL, asyncpg, SQLAlchemy 2.x async sessions, Pydantic v2, and Alembic's async migration runner. Database access is asynchronous; there is no synchronous ORM session or psycopg driver.

## Requirements

- Python 3.11+
- PostgreSQL 14+
- PowerShell on Windows (commands below)

## Docker development stack

From the repository root, start PostgreSQL, apply Alembic migrations, seed 20 clearly labeled synthetic profiles, and serve the frontend/API:

```powershell
docker compose up --build
```

Open `http://localhost:8080`; API docs are available at `http://localhost:8080/docs`. The API is also available locally at `http://localhost:8001`; this avoids the default port 8000, which may be used by another local project. The Compose stack binds web and API ports to localhost and does not publish PostgreSQL. Its fallback password is for local development only. Set a strong `POSTGRES_PASSWORD` in the root environment before sharing or deploying the stack. Demo seeding refuses to run unless `APP_ENV=development`.

The 20 representative profiles are fictional and do not describe real people or custody situations. Their illustrative SVG portraits are stored as bytes in PostgreSQL; they are not photographs. Replace them only with verified information and documented consent. The schema deliberately omits detention location, personal identity numbers, and family contact details.

Development action flows are intentionally limited to representative profiles: match requests are stored as pending, spiritual notes remain hidden until moderated, and contribution buttons are idempotent. The downloadable action guide is available only after a match is approved and is a clearly marked starting draft, not legal or operational advice. Production moderation, authentication, rate limiting, consent review, and a formally approved guide are required before enabling these flows for real profiles.

For a local, non-Docker setup, install requirements in a Python 3.11+ environment, provide a PostgreSQL database, and set `DATABASE_URL` to a `postgresql+asyncpg://` URL. If the URL is omitted, the application composes one from the `POSTGRES_*` settings.

Create the PostgreSQL role and database if they do not already exist (run in `psql` as a PostgreSQL administrator, replacing the password):

```sql
CREATE ROLE identity_chain LOGIN PASSWORD 'replace-with-a-strong-password';
CREATE DATABASE identity_chain OWNER identity_chain;
```

Apply the checked-in migration, seed development-only demo records, and start the API:

```powershell
alembic upgrade head
python -m app.seed_demo_data
uvicorn app.main:app --reload
```

Run Alembic and Uvicorn while the shell is in `backend`, where `alembic.ini` and the `app` package are located. The async Alembic environment is already configured in `alembic/env.py`; do not run `alembic init` over this existing configuration.

- Health endpoint: `http://127.0.0.1:8000/api/v1/health`
- OpenAPI docs: `http://127.0.0.1:8000/docs`

The health route returns HTTP 200 when `SELECT 1` succeeds and HTTP 503 when the database is unavailable. Responses use `{ "success": boolean, "data": object | null, "error": object | null }`.

## Architecture

- `app/v1/endpoints/`: HTTP routing, validation, and response mapping.
- `app/services/`: async database operations and domain logic.
- `app/schemas/`: Pydantic v2 request/response DTOs.
- `app/models/`: SQLAlchemy 2.x mapped entities.
- `app/db/base.py`: shared `DeclarativeBase` and model imports used by Alembic autogenerate.
- `app/db/session.py`: async engine, session factory, and `get_db` dependency.
- `app/core/config.py`: validated environment settings.
- `alembic/env.py`: async migration runner using `Base.metadata` and the configured async URL.

When adding a model, import it from `app/db/base.py` so Alembic discovers it, then create and apply a migration:

```powershell
alembic revision --autogenerate -m "describe schema change"
alembic upgrade head
```
