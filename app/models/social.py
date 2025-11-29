from app.database import Base
from sqlalchemy import Column, DateTime, Text, Integer
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("contents.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    content = Column(Text, nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Content", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("contents.id"), nullable=False)

    user = relationship("User", back_populates="likes")
    post = relationship("Content", back_populates="likes")