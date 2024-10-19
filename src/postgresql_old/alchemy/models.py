# Here we will store all the models (Tables structure) for the postgresql database

# access db by running docker exec -it svt-postgres-1 psql -U admin -d svt in root

from sqlalchemy import Column, Integer, String, Boolean, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TikTokVideo(Base):
    __tablename__ = 'tiktok_videos'

    id = Column(String, primary_key=True)
    desc = Column(String)
    create_time = Column(BigInteger)
    author_id = Column(String, ForeignKey('authors.id'))
    music_id = Column(String, ForeignKey('music.id'))
    stats = Column(JSON)
    
    author = relationship("Author", back_populates="videos")
    music = relationship("Music", back_populates="videos")
    challenges = relationship("Challenge", secondary="video_challenges", back_populates="videos")

class Author(Base):
    __tablename__ = 'authors'

    id = Column(String, primary_key=True)
    nickname = Column(String)
    unique_id = Column(String)
    signature = Column(String)
    verified = Column(Boolean)
    stats = Column(JSON)

    videos = relationship("TikTokVideo", back_populates="author")

class Music(Base):
    __tablename__ = 'music'

    id = Column(String, primary_key=True)
    title = Column(String)
    author_name = Column(String)
    duration = Column(Integer)
    original = Column(Boolean)

    videos = relationship("TikTokVideo", back_populates="music")

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(String, primary_key=True)
    title = Column(String)
    desc = Column(String)

    videos = relationship("TikTokVideo", secondary="video_challenges", back_populates="challenges")

class VideoChallenge(Base):
    __tablename__ = 'video_challenges'

    video_id = Column(String, ForeignKey('tiktok_videos.id'), primary_key=True)
    challenge_id = Column(String, ForeignKey('challenges.id'), primary_key=True)