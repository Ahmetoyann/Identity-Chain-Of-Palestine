import asyncio

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.item import Prisoner
from app.demo_profiles import build_demo_profiles


async def seed_demo_profiles() -> None:
	if settings.app_env != "development":
		raise RuntimeError("Demo data can only be seeded when APP_ENV=development")

	async with AsyncSessionLocal() as session:
		statement = insert(Prisoner).values(build_demo_profiles())
		update_fields = (
			"name",
			"profession",
			"short_bio",
			"biography",
			"status",
			"dreams",
			"image_url",
			"image_data",
			"image_media_type",
			"is_demo",
			"is_published",
		)
		statement = statement.on_conflict_do_update(
			index_elements=["slug"],
			set_={
				**{field: getattr(statement.excluded, field) for field in update_fields},
				"updated_at": func.now(),
			},
		)
		await session.execute(statement)
		await session.commit()


if __name__ == "__main__":
	asyncio.run(seed_demo_profiles())