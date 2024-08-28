from typing import Annotated
from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserOut
from config import settings
from database import get_async_session
from exceptions import (
    IncorrectTokenException,
    NotAccessErrorException,
    UnauthorizedUserException,
    TokenExpiredException,
    TokenAbsentException,
)
from src.services.user import UserService
from src.repositories.user import UserRepository


def get_token(request: Request):
    token: str = request.cookies.get("user_access_token")
    if not token:
        return None
    return token


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(get_token)],
) -> UserOut:
    if not token:
        raise TokenAbsentException
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenException
    user_id: str = payload.get("sub")
    if not user_id:
        raise NotAccessErrorException
    user = await UserService(user_repository=UserRepository).get_user(
        session=session, id=int(user_id)
    )
    if not user:
        raise UnauthorizedUserException
    return user
