from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0005_volunteer_draw_actions"
down_revision = "0004_representative_portraits"
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		"volunteer_matches",
		sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("visitor_id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("prisoner_id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("status", sa.String(length=20), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.ForeignKeyConstraint(["prisoner_id"], ["prisoners.id"], ondelete="RESTRICT"),
		sa.PrimaryKeyConstraint("id"),
	)
	op.create_index("ix_volunteer_matches_visitor_id", "volunteer_matches", ["visitor_id"])
	op.create_index("ix_volunteer_matches_prisoner_id", "volunteer_matches", ["prisoner_id"])
	op.create_table(
		"volunteer_actions",
		sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("match_id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("action_type", sa.String(length=20), nullable=False),
		sa.Column("content", sa.Text(), nullable=True),
		sa.Column("idempotency_key", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.CheckConstraint(
			"action_type IN ('prayer', 'good_deed', 'note', 'share')",
			name="ck_volunteer_actions_action_type",
		),
		sa.ForeignKeyConstraint(["match_id"], ["volunteer_matches.id"], ondelete="CASCADE"),
		sa.PrimaryKeyConstraint("id"),
		sa.UniqueConstraint("match_id", "idempotency_key", name="uq_volunteer_action_idempotency"),
	)
	op.create_index("ix_volunteer_actions_match_id", "volunteer_actions", ["match_id"])


def downgrade() -> None:
	op.drop_index("ix_volunteer_actions_match_id", table_name="volunteer_actions")
	op.drop_table("volunteer_actions")
	op.drop_index("ix_volunteer_matches_prisoner_id", table_name="volunteer_matches")
	op.drop_index("ix_volunteer_matches_visitor_id", table_name="volunteer_matches")
	op.drop_table("volunteer_matches")
