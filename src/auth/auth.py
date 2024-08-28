from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserOut
from config import settings
from database import get_async_session
from exceptions import IncorrectUsernameOrPasswordException
from src.repositories.user import UserRepository
from src.services.user import UserService


pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return encode_jwt


async def authenticate_user(
    username: str,
    password: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserOut:
    user: User = await UserService(user_repository=UserRepository).get_user(
        session=session, username=username
    )
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectUsernameOrPasswordException
    return user
