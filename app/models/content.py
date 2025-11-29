from app.database import Base
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

import uuid

class Content(Base):
    __tablename__ = "contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    posted_at = Column(DateTime, default=datetime.now(), nullable=False)

    user = relationship("User", back_populates="contents")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    content_type = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': content_type
    }
    


class News(Content):
    __tablename__ = "news"

    id = Column(UUID(as_uuid=True), ForeignKey("contents.id"), primary_key=True)
    full_url = Column(String, nullable=False)


    __mapper_args__ = {
        'polymorphic_identity': 'news',
    }


class Event(Content):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), ForeignKey("contents.id"), primary_key=True)
    event_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)

    full_url = Column(String, nullable=False)

    participants = relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'event',
    }

class PhotoGallery(Content):
    __tablename__ = "photo_galleries"

    id = Column(UUID(as_uuid=True), ForeignKey("contents.id"), primary_key=True)
    file_url = Column(String, nullable=False)  

    __mapper_args__ = {
        'polymorphic_identity': 'photo_gallery',
    }

class EventParticipant(Base):
    __tablename__ = "event_participants"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True,  nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), primary_key=True,  nullable=False)

    user = relationship("User", back_populates="event_participations")
    event = relationship("Event", back_populates="participants")