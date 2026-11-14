import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, LargeBinary, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Prisoner(Base):
	__tablename__ = "prisoners"

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
	name: Mapped[str] = mapped_column(String(160), nullable=False)
	profession: Mapped[str] = mapped_column(String(120), nullable=False)
	short_bio: Mapped[str] = mapped_column(String(240), nullable=False)
	biography: Mapped[str] = mapped_column(Text, nullable=False)
	status: Mapped[str] = mapped_column(String(40), nullable=False, default="not_shared")
	image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
	image_data: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
	image_media_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
	dreams: Mapped[str | None] = mapped_column(Text, nullable=True)
	prayers_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
	good_deeds_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
	is_demo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	is_matched: Mapped[bool] = mapped_column(
		Boolean, nullable=False, default=False, server_default=text("false")
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
	)


class ContactMessage(Base):
	__tablename__ = "contact_messages"

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	name: Mapped[str] = mapped_column(String(120), nullable=False)
	email: Mapped[str] = mapped_column(String(320), nullable=False)
	subject: Mapped[str] = mapped_column(String(120), nullable=False)
	message: Mapped[str] = mapped_column(Text, nullable=False)
	consent: Mapped[bool] = mapped_column(Boolean, nullable=False)
	status: Mapped[str] = mapped_column(String(20), nullable=False, default="new")
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
	)
