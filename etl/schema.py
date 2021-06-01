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


class YoutubePlaylist(Base):
    __tablename__ = 'youtube_playlists'
    id = Column(Integer, primary_key=True)
    youtube_id = Column(String, nullable=False, unique=True)





