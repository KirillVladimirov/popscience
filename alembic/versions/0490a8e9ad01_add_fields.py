from alembic import op
import sqlalchemy as sa


revision = '0490a8e9ad01'
down_revision = '79ab43cbd198'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('youtube_videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('origin_url', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('rating', sa.String(), nullable=True),
    sa.Column('platform', sa.String(), nullable=True),
    sa.Column('theme', sa.String(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('captions_xml', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['youtube_channels.id'], name=op.f('fk__youtube_videos__channel_id__youtube_channels')),
    sa.ForeignKeyConstraint(['playlist_id'], ['youtube_playlists.id'], name=op.f('fk__youtube_videos__playlist_id__youtube_playlists')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__youtube_videos')),
    sa.UniqueConstraint('origin_url', name=op.f('uq__youtube_videos__origin_url'))
    )
    op.add_column('youtube_playlists', sa.Column('youtube_playlist_id', sa.String(), nullable=False))
    op.add_column('youtube_playlists', sa.Column('title', sa.String(), nullable=True))
    op.add_column('youtube_playlists', sa.Column('description', sa.String(), nullable=True))
    op.add_column('youtube_playlists', sa.Column('views', sa.String(), nullable=True))
    op.drop_constraint('uq__youtube_playlists__playlist_id', 'youtube_playlists', type_='unique')
    op.create_unique_constraint(op.f('uq__youtube_playlists__youtube_playlist_id'), 'youtube_playlists', ['youtube_playlist_id'])
    op.drop_column('youtube_playlists', 'playlist_id')


def downgrade():
    op.add_column('youtube_playlists', sa.Column('playlist_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('uq__youtube_playlists__youtube_playlist_id'), 'youtube_playlists', type_='unique')
    op.create_unique_constraint('uq__youtube_playlists__playlist_id', 'youtube_playlists', ['playlist_id'])
    op.drop_column('youtube_playlists', 'views')
    op.drop_column('youtube_playlists', 'description')
    op.drop_column('youtube_playlists', 'title')
    op.drop_column('youtube_playlists', 'youtube_playlist_id')
    op.drop_table('youtube_videos')
