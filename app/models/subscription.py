from sqlalchemy import Column, Integer, String, Decimal, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

import uuid
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Decimal, nullable=False)
    discount = Column(Decimal, nullable=True)
    student_discount = Column(Decimal, nullable=True)

    profiles = relationship("UserProfile", back_populates="subscription")
