from alembic import op
import sqlalchemy as sa


revision = 'e72c566a4f20'
down_revision = 'e2682f83f500'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('youtube_videos', sa.Column('views', sa.String(), nullable=True))
    op.drop_column('youtube_videos', 'platform')


def downgrade():
    op.add_column('youtube_videos', sa.Column('platform', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('youtube_videos', 'views')
