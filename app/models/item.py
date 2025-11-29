import uuid
from app.database import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    serial_number = Column(String, nullable=False)
    description = Column(String, nullable=True)
    received_at = Column(DateTime, nullable=True)
    for_rent = Column(Boolean, default=True)

    user = relationship("User", back_populates="items")
    loans = relationship("Loan", back_populates="item", cascade="all, delete-orphan")
    loan_queue = relationship("LoanQueue", back_populates="item", cascade="all, delete-orphan")
