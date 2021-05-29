import sqlalchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey


convention = {
    "all_column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s"
}

metadata = sqlalchemy.MetaData(naming_convention=convention)

youtube_channels = Table(
    'youtube_channels',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('ulr', String, nullable=False, unique=True),
)

youtube_playlists = Table(
    "youtube_playlists",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('channel_id', ForeignKey('youtube_channels.id'), nullable=False),
    Column('youtube_playlist_id', String, nullable=False, unique=True),
    Column('title', String),
    Column('description', String),
    Column('views', String),
)

youtube_videos = Table(
    "youtube_videos",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('channel_id', ForeignKey('youtube_channels.id'), nullable=False),
    Column('playlist_id', ForeignKey('youtube_playlists.id'), nullable=False),
    Column('origin_url', String, nullable=False, unique=True),
    Column('title', String),
    Column('date', String),
    Column('duration', String),
    Column('author', String),
    Column('tags', String),
    Column('about', String),
    Column('rating', String),
    Column('platform', String),
    Column('theme', String),
    Column('language', String),
    Column('captions_xml', String),
)






