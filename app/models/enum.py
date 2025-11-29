import enum

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LoanStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    EXPIRED = "expired"
    LOST = "lost"
    DAMAGED = "damaged"