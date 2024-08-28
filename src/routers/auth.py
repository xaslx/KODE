from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.schemas.user import UserAdd, UserOut
from database import get_async_session
from exceptions import UserAlreadyExistsException, UserNotFoundException
from typing import Annotated
from src.services.user import UserService
from src.services.dependencies import get_user_service
from fastapi_versioning import version


auth_router: APIRouter = APIRouter(
    prefix="/api/auth", tags=["Аутентификация и Авторизация"]
)


@auth_router.post("/register", status_code=201)
@version(1)
async def rigister_user(
    user: UserAdd,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserOut:
    exist_user: UserOut | None = await user_service.get_user(
        session=session, username=user.username
    )
    if exist_user:
        raise UserAlreadyExistsException
    hashed_password: str = get_password_hash(user.password)
    new_user: UserOut = await user_service.add_new_user(
        session=session,
        username=user.username,
        hashed_password=hashed_password,
    )
    return new_user


@auth_router.post("/login", status_code=200)
@version(1)
async def login_user(
    response: Response,
    user: UserAdd,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    user: UserOut = await authenticate_user(
        user.username, user.password, session=session
    )

    if not user:
        raise UserNotFoundException

    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie("user_access_token", access_token, httponly=True)
    return access_token


@auth_router.post("/logout", status_code=200)
@version(1)
async def logout_user(response: Response) -> int:
    response.delete_cookie("user_access_token")
    return 200
