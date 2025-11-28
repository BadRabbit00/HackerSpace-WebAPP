from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
import uuid


from app.dependencies import get_db
from app.schemas.users import UserCreate, UserResponse, UserUpdate, UserLogin, Token
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token


router = APIRouter(prefix="/users")


@router.post("/create", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user."""
    
    query = select(User).where(User.email == user.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_pw = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_pw,
        is_active=True,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})

    new_user.refresh_token = refresh_token
    await db.commit()

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """User login endpoint (to be implemented)."""
    query = select(User).where(
        or_(User.email == user.identifier, 
            User.username == user.identifier
        )
    )
    
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or user does not exist"
        )
    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

    db_user.refresh_token = refresh_token
    await db.commit()

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh/token", response_model=Token)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to refresh access token using a valid refresh token.
    """
    # 1. Декодируем токен
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token payload"
        )
    
    query = select(User).where(User.id == uuid.UUID(user_id))
    result = await db.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user or db_user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    new_access_token = create_access_token(data={"sub": str(user_id)})
    
    return Token(access_token=new_access_token, refresh_token=refresh_token, token_type="bearer")    