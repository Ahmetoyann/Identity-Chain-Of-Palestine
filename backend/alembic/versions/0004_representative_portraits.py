from alembic import op
import sqlalchemy as sa

revision = "0004_representative_portraits"
down_revision = "0003_community_actions"
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.add_column("prisoners", sa.Column("image_data", sa.LargeBinary(), nullable=True))
	op.add_column("prisoners", sa.Column("image_media_type", sa.String(length=100), nullable=True))


def downgrade() -> None:
	op.drop_column("prisoners", "image_media_type")
	op.drop_column("prisoners", "image_data")