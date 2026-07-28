from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email.lower()))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    user = User(email=str(payload.email).lower(), hashed_password=hash_password(payload.password), full_name=payload.full_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user is None or not user.is_active or not verify_password(password, user.hashed_password):
        return None
    return user
