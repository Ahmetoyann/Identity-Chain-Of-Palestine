from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
	pass


# Import models after Base is declared so Alembic sees all mapped tables.
from app.models.user import User  # noqa: E402,F401

__all__ = ["Base", "User"]
