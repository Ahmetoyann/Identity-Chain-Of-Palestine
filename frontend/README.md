# Identity Chain Frontend

React frontend for the Identity Chain archive. The archive is served by FastAPI and PostgreSQL; starting React by itself does not create or seed archive records.

## Run the complete local stack

From the repository root, with Docker Desktop running:

```powershell
docker compose up --build
```

Open `http://localhost:8080`. The API applies its Alembic migration and inserts 20 clearly labeled synthetic demo profiles before it starts. API docs are available at `http://localhost:8080/docs`.

Stop the stack with `Ctrl+C`, then run `docker compose down` from the repository root. The PostgreSQL volume is retained, so records remain on the next start.

## Run React separately

`npm start` serves the frontend on port 3000 and proxies `/api` requests to `http://localhost:8001`, the Compose API port. Start PostgreSQL and the backend first. Restart the React development server if the proxy setting was changed while it was running.

The archive must not be used with real people until identity verification, informed consent, publication review, and data-protection procedures are in place. Demo profiles are fictional test fixtures.