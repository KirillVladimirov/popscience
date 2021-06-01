"""create_youtube_videos

Revision ID: e2682f83f500
Revises: 6ea9e42513c1
Create Date: 2021-06-01 09:22:57.535246

"""
from alembic import op
import sqlalchemy as sa


revision = 'e2682f83f500'
down_revision = '6ea9e42513c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('youtube_videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('playlist_id', sa.Integer(), nullable=True),
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


def downgrade():
    op.drop_table('youtube_videos')
