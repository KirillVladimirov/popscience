
from alembic import op
import sqlalchemy as sa

revision = '79ab43cbd198'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('youtube_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ulr', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__youtube_channels')),
    sa.UniqueConstraint('ulr', name=op.f('uq__youtube_channels__ulr'))
    )
    op.create_table('youtube_playlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('playlist_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['youtube_channels.id'], name=op.f('fk__youtube_playlists__channel_id__youtube_channels')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__youtube_playlists')),
    sa.UniqueConstraint('playlist_id', name=op.f('uq__youtube_playlists__playlist_id'))
    )


def downgrade():
    op.drop_table('youtube_playlists')
    op.drop_table('youtube_channels')
