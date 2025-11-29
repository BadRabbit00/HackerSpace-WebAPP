from app.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Enum as SAEnum
from sqlalchemy import ForeignKey
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .enum import LoanStatus

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    status = Column(SAEnum(LoanStatus), default=LoanStatus.PENDING, nullable=False)
    reason = Column(String, nullable=False)
    document_receipt = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    received_at = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=False)
    returned_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="loans")
    item = relationship("Item", back_populates="loans")



class LoanQueue(Base):
    __tablename__ = "loan_queue"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    load_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="loan_queue")
    item = relationship("Item", back_populates="loan_queue")