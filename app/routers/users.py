"""
Users router with example CRUD operations.
"""
from threading import Lock
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter(prefix="/users")


# Pydantic models for request/response
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# In-memory storage for demo purposes
# Replace with actual database operations in production
_users_db: dict = {}
_user_id_counter: int = 1
_user_lock = Lock()


@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """List all users with pagination."""
    users = list(_users_db.values())
    return users[skip : skip + limit]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Create a new user."""
    global _user_id_counter

    with _user_lock:
        # Check if email already exists
        for existing_user in _users_db.values():
            if existing_user["email"] == user.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        user_data = {
            "id": _user_id_counter,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_active": True,
        }
        _users_db[_user_id_counter] = user_data
        _user_id_counter += 1

    return user_data


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get a specific user by ID."""
    if user_id not in _users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _users_db[user_id]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Update a user."""
    if user_id not in _users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user = _users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        user[field] = value

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a user."""
    if user_id not in _users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    del _users_db[user_id]
