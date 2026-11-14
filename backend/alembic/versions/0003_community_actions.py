from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003_community_actions"
down_revision = "0002_contact_messages"
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.add_column(
		"prisoners",
		sa.Column("is_matched", sa.Boolean(), server_default=sa.false(), nullable=False),
	)
	op.create_table(
		"match_requests",
		sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("prisoner_id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("full_name", sa.String(length=120), nullable=False),
		sa.Column("email", sa.String(length=320), nullable=False),
		sa.Column("consent", sa.Boolean(), nullable=False),
		sa.Column("status", sa.String(length=20), nullable=False),
		sa.Column("is_demo", sa.Boolean(), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
	sa.ForeignKeyConstraint(["prisoner_id"], ["prisoners.id"], ondelete="RESTRICT"),
		sa.PrimaryKeyConstraint("id"),
	)
	op.create_index("ix_match_requests_prisoner_id", "match_requests", ["prisoner_id"])
	op.create_table(
		"spiritual_notes",
		sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("prisoner_id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("display_name", sa.String(length=80), nullable=True),
		sa.Column("message", sa.Text(), nullable=False),
		sa.Column("consent", sa.Boolean(), nullable=False),
		sa.Column("status", sa.String(length=20), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.ForeignKeyConstraint(["prisoner_id"], ["prisoners.id"], ondelete="RESTRICT"),
		sa.PrimaryKeyConstraint("id"),
	)
	op.create_index("ix_spiritual_notes_prisoner_id", "spiritual_notes", ["prisoner_id"])
	op.create_table(
		"contributions",
		sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("prisoner_id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("action_type", sa.String(length=20), nullable=False),
		sa.Column("idempotency_key", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.CheckConstraint("action_type IN ('prayer', 'good_deed')", name="ck_contributions_action_type"),
		sa.ForeignKeyConstraint(["prisoner_id"], ["prisoners.id"], ondelete="RESTRICT"),
		sa.PrimaryKeyConstraint("id"),
		sa.UniqueConstraint("idempotency_key", name="uq_contributions_idempotency_key"),
	)
	op.create_index("ix_contributions_prisoner_id", "contributions", ["prisoner_id"])


def downgrade() -> None:
	op.drop_index("ix_contributions_prisoner_id", table_name="contributions")
	op.drop_table("contributions")
	op.drop_index("ix_spiritual_notes_prisoner_id", table_name="spiritual_notes")
	op.drop_table("spiritual_notes")
	op.drop_index("ix_match_requests_prisoner_id", table_name="match_requests")
	op.drop_table("match_requests")
	op.drop_column("prisoners", "is_matched")