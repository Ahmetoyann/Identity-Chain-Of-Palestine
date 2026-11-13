from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=BACKEND_ROOT / ".env",
		env_file_encoding="utf-8",
		case_sensitive=False,
		extra="ignore",
	)

	app_name: str = "Identity Chain API"
	app_env: Literal["development", "test", "production"] = "development"
	debug: bool = False
	log_level: str = "INFO"

	database_url: str = Field(default="", repr=False)
	postgres_user: str | None = None
	postgres_password: SecretStr | None = Field(default=None, repr=False)
	postgres_db: str | None = None
	postgres_host: str = "localhost"
	postgres_port: int = Field(default=5432, ge=1, le=65535)

	cors_origins: list[str] = Field(
		default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
	)
	db_pool_size: int = Field(default=10, ge=1)
	db_max_overflow: int = Field(default=20, ge=0)
	db_pool_recycle_seconds: int = Field(default=1800, ge=1)

	@model_validator(mode="after")
	def configure_async_database_url(self) -> "Settings":
		if self.database_url:
			parsed_url = make_url(self.database_url)
			if parsed_url.drivername != "postgresql+asyncpg":
				raise ValueError("DATABASE_URL must use postgresql+asyncpg")
			return self

		missing = [
			name
			for name, value in (
				("POSTGRES_USER", self.postgres_user),
				("POSTGRES_PASSWORD", self.postgres_password),
				("POSTGRES_DB", self.postgres_db),
			)
			if value is None
		]
		if missing:
			raise ValueError(
				"Set DATABASE_URL or provide: " + ", ".join(missing)
			)

		self.database_url = URL.create(
			drivername="postgresql+asyncpg",
			username=self.postgres_user,
			password=self.postgres_password.get_secret_value(),
			host=self.postgres_host,
			port=self.postgres_port,
			database=self.postgres_db,
		).render_as_string(hide_password=False)
		return self


@lru_cache
def get_settings() -> Settings:
	return Settings()


settings = get_settings()
