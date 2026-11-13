from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.db.session import engine
from app.v1.api import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
	yield
	await engine.dispose()


app = FastAPI(
	title=settings.app_name,
	debug=settings.debug,
	lifespan=lifespan,
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_origins,
	allow_credentials=True,
	allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
	allow_headers=["Authorization", "Content-Type", "Accept"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
	_: Request, exc: StarletteHTTPException
) -> JSONResponse:
	return JSONResponse(
		status_code=exc.status_code,
		content={"success": False, "data": None, "error": {"message": exc.detail}},
		headers=exc.headers,
	)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
	_: Request, exc: RequestValidationError
) -> JSONResponse:
	errors: list[dict[str, Any]] = [
		{"location": list(error["loc"]), "message": error["msg"], "type": error["type"]}
		for error in exc.errors()
	]
	return JSONResponse(
		status_code=422,
		content={
			"success": False,
			"data": None,
			"error": {"message": "Request validation failed", "details": errors},
		},
	)


app.include_router(api_router, prefix="/api/v1")
