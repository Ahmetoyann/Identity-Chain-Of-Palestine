from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_contact_messages"
down_revision = "0001_initial_archive"
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table(
		"contact_messages",
		sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
		sa.Column("name", sa.String(length=120), nullable=False),
		sa.Column("email", sa.String(length=320), nullable=False),
		sa.Column("subject", sa.String(length=120), nullable=False),
		sa.Column("message", sa.Text(), nullable=False),
		sa.Column("consent", sa.Boolean(), nullable=False),
		sa.Column("status", sa.String(length=20), nullable=False),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
		sa.PrimaryKeyConstraint("id"),
	)
	op.create_index("ix_contact_messages_created_at", "contact_messages", ["created_at"])


def downgrade() -> None:
	op.drop_index("ix_contact_messages_created_at", table_name="contact_messages")
	op.drop_table("contact_messages")