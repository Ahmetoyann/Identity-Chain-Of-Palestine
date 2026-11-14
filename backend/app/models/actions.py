import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class MatchRequest(Base):
	__tablename__ = "match_requests"

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	prisoner_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), ForeignKey("prisoners.id", ondelete="RESTRICT"), index=True, nullable=False
	)
	full_name: Mapped[str] = mapped_column(String(120), nullable=False)
	email: Mapped[str] = mapped_column(String(320), nullable=False)
	consent: Mapped[bool] = mapped_column(Boolean, nullable=False)
	status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
	is_demo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)


class SpiritualNote(Base):
	__tablename__ = "spiritual_notes"

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	prisoner_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), ForeignKey("prisoners.id", ondelete="RESTRICT"), index=True, nullable=False
	)
	display_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
	message: Mapped[str] = mapped_column(Text, nullable=False)
	consent: Mapped[bool] = mapped_column(Boolean, nullable=False)
	status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)


class Contribution(Base):
	__tablename__ = "contributions"
	__table_args__ = (
		CheckConstraint("action_type IN ('prayer', 'good_deed')", name="ck_contributions_action_type"),
		UniqueConstraint("idempotency_key", name="uq_contributions_idempotency_key"),
	)

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	prisoner_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), ForeignKey("prisoners.id", ondelete="RESTRICT"), index=True, nullable=False
	)
	action_type: Mapped[str] = mapped_column(String(20), nullable=False)
	idempotency_key: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)


class VolunteerMatch(Base):
	__tablename__ = "volunteer_matches"

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	visitor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
	prisoner_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), ForeignKey("prisoners.id", ondelete="RESTRICT"), index=True, nullable=False
	)
	status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)


class VolunteerAction(Base):
	__tablename__ = "volunteer_actions"
	__table_args__ = (
		CheckConstraint(
			"action_type IN ('prayer', 'good_deed', 'note', 'share')",
			name="ck_volunteer_actions_action_type",
		),
		UniqueConstraint("match_id", "idempotency_key", name="uq_volunteer_action_idempotency"),
	)

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	match_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True), ForeignKey("volunteer_matches.id", ondelete="CASCADE"), index=True, nullable=False
	)
	action_type: Mapped[str] = mapped_column(String(20), nullable=False)
	content: Mapped[str | None] = mapped_column(Text, nullable=True)
	idempotency_key: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)