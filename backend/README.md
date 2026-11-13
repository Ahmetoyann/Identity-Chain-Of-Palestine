# Identity Chain API

FastAPI backend using PostgreSQL, asyncpg, SQLAlchemy 2.x async sessions, Pydantic v2, and Alembic's async migration runner. Database access is asynchronous; there is no synchronous ORM session or psycopg driver.

## Requirements

- Python 3.11+
- PostgreSQL 14+
- PowerShell on Windows (commands below)

## Windows setup

Run commands from the repository root:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set a strong `POSTGRES_PASSWORD`. `DATABASE_URL` must use `postgresql+asyncpg://`. If the URL is omitted, the application composes one from the `POSTGRES_*` settings.

Create the PostgreSQL role and database if they do not already exist (run in `psql` as a PostgreSQL administrator, replacing the password):

```sql
CREATE ROLE identity_chain LOGIN PASSWORD 'replace-with-a-strong-password';
CREATE DATABASE identity_chain OWNER identity_chain;
```

Apply the first migration and start the API:

```powershell
alembic revision --autogenerate -m "create users table"
alembic upgrade head
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
