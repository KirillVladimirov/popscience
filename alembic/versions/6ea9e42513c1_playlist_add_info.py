from alembic import op
import sqlalchemy as sa


revision = '6ea9e42513c1'
down_revision = '62b62aeacdeb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('youtube_playlists', sa.Column('title', sa.String(), nullable=True))
    op.add_column('youtube_playlists', sa.Column('description', sa.String(), nullable=True))
    op.add_column('youtube_playlists', sa.Column('views', sa.String(), nullable=True))


def downgrade():
    op.drop_column('youtube_playlists', 'views')
    op.drop_column('youtube_playlists', 'description')
    op.drop_column('youtube_playlists', 'title')
