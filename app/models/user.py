from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Text
from sqlalchemy.types import Enum as SAEnum

from app.database import Base 
from .enum import VerificationStatus

import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="user")
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    loan_queue = relationship("LoanQueue", back_populates="user", cascade="all, delete-orphan")
    verification_requests = relationship("VerificationRequest", back_populates="user", cascade="all, delete-orphan")
    contents = relationship("Content", back_populates="user", cascade="all, delete-orphan")
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")
    event_participations = relationship("EventParticipant", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, unique=True, nullable=False)
    subscription_type = Column(String, ForeignKey("subscriptions.name"), nullable=True)

    bio = Column(Text, nullable=True)
    avatar = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    telegram_link = Column(String, nullable=True)
    linkedin_link = Column(String, nullable=True)
    website_link = Column(String, nullable=True)

    user = relationship("User", back_populates="profile", uselist=False, cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="profiles", uselist=False, cascade="all, delete-orphan")




class UserPersonalData(Base):
    __tablename__ = "user_personal_data"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, unique=True, nullable=False)
    iin = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    date_of_birth = Column(String, nullable=True)
    document_front = Column(String, nullable=False)
    document_back = Column(String, nullable=True)
    student_id = Column(String, nullable=True)

    is_student = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="personal_data", cascade="all, delete-orphan")

class VerificationRequest(Base): 
    __tablename__ = "verification_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    verified_status = Column(SAEnum(VerificationStatus), nullable=False, default=VerificationStatus.PENDING)
    student_status = Column(SAEnum(VerificationStatus), nullable=False, default=VerificationStatus.PENDING)

    is_student = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="verification_requests", cascade="all, delete-orphan")