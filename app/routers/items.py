"""
Items router with example CRUD operations and Redis caching.
"""
import json
from threading import Lock
from typing import List, Optional

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_redis

router = APIRouter(prefix="/items")


# Pydantic models for request/response
class ItemBase(BaseModel):
    """Base item schema."""
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0


class ItemCreate(ItemBase):
    """Item creation schema."""
    pass


class ItemUpdate(BaseModel):
    """Item update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ItemResponse(ItemBase):
    """Item response schema."""
    id: int

    class Config:
        from_attributes = True


# In-memory storage for demo purposes
# Replace with actual database operations in production
_items_db: dict = {}
_item_id_counter: int = 1
_item_lock = Lock()


@router.get("", response_model=List[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """List all items with pagination."""
    items = list(_items_db.values())
    return items[skip : skip + limit]


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> dict:
    """Create a new item."""
    global _item_id_counter

    with _item_lock:
        item_data = {
            "id": _item_id_counter,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "quantity": item.quantity,
        }
        _items_db[_item_id_counter] = item_data
        current_id = _item_id_counter
        _item_id_counter += 1

    # Cache the item in Redis
    try:
        await redis_client.set(
            f"item:{current_id}",
            json.dumps(item_data),
            ex=3600,  # Expire in 1 hour
        )
    except Exception:
        pass  # Redis caching is optional

    return item_data


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> dict:
    """Get a specific item by ID with Redis caching."""
    # Try to get from Redis cache first
    try:
        cached = await redis_client.get(f"item:{item_id}")
        if cached:
            return json.loads(cached)
    except Exception:
        pass  # Fall back to in-memory storage

    if item_id not in _items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return _items_db[item_id]


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> dict:
    """Update an item."""
    if item_id not in _items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    item = _items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        item[field] = value

    # Update Redis cache
    try:
        await redis_client.set(
            f"item:{item_id}",
            json.dumps(item),
            ex=3600,
        )
    except Exception:
        pass

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> None:
    """Delete an item."""
    if item_id not in _items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    del _items_db[item_id]

    # Remove from Redis cache
    try:
        await redis_client.delete(f"item:{item_id}")
    except Exception:
        pass
