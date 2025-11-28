from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Text

from app.database import Base 

import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String, nullable=True)

    profile = relationship("UserProfile", uselist=False, back_populates="user")


class UserProfile(Base):
    __tablename__ = "profiles"

    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)

    github_link = Column(String, nullable=True)
    telegram_link = Column(String, nullable=True)
    linkedin_link = Column(String, nullable=True)
    website_link = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")

class UserPersonalData(Base):
    __tablename__ = "user_personal_data"

    data_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)

    user = relationship("User", back_populates="personal_data")