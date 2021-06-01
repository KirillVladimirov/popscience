import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


convention = {
    "all_column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s"
}

metadata = sqlalchemy.MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)
engine = create_engine("postgresql://postgres:@localhost:5432/university2035_etl", echo=True)
Session = sessionmaker(bind=engine)


class YoutubeChannel(Base):
    __tablename__ = 'youtube_channels'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    playlists = relationship("YoutubePlaylist", backref="channel")


class YoutubePlaylist(Base):
    __tablename__ = 'youtube_playlists'
    id = Column(Integer, primary_key=True)
    youtube_id = Column(String, nullable=False, unique=True)
    channel_id = Column(Integer, ForeignKey('youtube_channels.id'))
    title = Column(String)
    description = Column(String)
    views = Column(String)


class YoutubeVideo(Base):
    __tablename__ = 'youtube_videos'
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('youtube_channels.id'))
    playlist_id = Column(Integer, ForeignKey('youtube_playlists.id'))
    origin_url = Column(String, nullable=False, unique=True)
    title = Column(String)
    date = Column(String)
    duration = Column(String)
    author = Column(String)
    tags = Column(String)
    about = Column(String)
    rating = Column(String)
    views = Column(String)
    theme = Column(String)
    language = Column(String)
    captions_xml = Column(String)


#
# youtube_videos = Table(
#     "youtube_videos",
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('channel_id', ForeignKey('youtube_channels.id'), nullable=False),
#     Column('playlist_id', ForeignKey('youtube_playlists.id'), nullable=False),
#     Column('origin_url', String, nullable=False, unique=True),
#     Column('title', String),
#     Column('date', String),
#     Column('duration', String),
#     Column('author', String),
#     Column('tags', String),
#     Column('about', String),
#     Column('rating', String),
#     Column('platform', String),
#     Column('theme', String),
#     Column('language', String),
#     Column('captions_xml', String),
# )


