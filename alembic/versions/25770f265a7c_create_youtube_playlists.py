from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25770f265a7c'
down_revision = 'c8ac14f4ea7f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('youtube_playlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('youtube_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__youtube_playlists')),
    sa.UniqueConstraint('youtube_id', name=op.f('uq__youtube_playlists__youtube_id'))
    )


def downgrade():
    op.drop_table('youtube_playlists')
