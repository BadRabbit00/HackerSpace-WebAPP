from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    """
    Схема специально для входа.
    Ничего лишнего, только креды.
    """
    identifier: str 
    password: str

class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

class Token(BaseModel):
    """
    Схема для ответа при успешном логине.
    """
    access_token: str
    refresh_token: str
    token_type: str

class UserResponse(UserBase):
    """User response schema."""
    id: UUID
    is_active: bool = True

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    """User creation schema."""
    password: str