from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_archive"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		"users",
		sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
		sa.Column("email", sa.String(length=320), nullable=False),
		sa.Column("full_name", sa.String(length=200), nullable=False),
		sa.Column("is_active", sa.Boolean(), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
	)
	op.create_index("ix_users_email", "users", ["email"], unique=True)
	op.create_table(
		"prisoners",
		sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
		sa.Column("slug", sa.String(length=100), nullable=False),
		sa.Column("name", sa.String(length=160), nullable=False),
		sa.Column("profession", sa.String(length=120), nullable=False),
		sa.Column("short_bio", sa.String(length=240), nullable=False),
		sa.Column("biography", sa.Text(), nullable=False),
		sa.Column("status", sa.String(length=40), nullable=False),
		sa.Column("image_url", sa.String(length=500), nullable=True),
		sa.Column("dreams", sa.Text(), nullable=True),
		sa.Column("prayers_count", sa.Integer(), nullable=False),
		sa.Column("good_deeds_count", sa.Integer(), nullable=False),
		sa.Column("is_demo", sa.Boolean(), nullable=False),
		sa.Column("is_published", sa.Boolean(), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
	)
	op.create_index("ix_prisoners_slug", "prisoners", ["slug"], unique=True)


def downgrade() -> None:
	op.drop_index("ix_prisoners_slug", table_name="prisoners")
	op.drop_table("prisoners")
	op.drop_index("ix_users_email", table_name="users")
	op.drop_table("users")