from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserOut
from src.repositories.user import UserRepository


class UserService:

    def __init__(self, user_repository: type[UserRepository]) -> None:
        self.user_repository = user_repository()

    async def add_new_user(
        self, session: AsyncSession, username: str, hashed_password: str
    ) -> UserOut:
        new_user: UserOut = await self.user_repository.add(
            session=session, username=username, hashed_password=hashed_password
        )
        return new_user

    async def get_user(self, session: AsyncSession, **filter_by) -> UserOut:
        user: UserOut = await self.user_repository.find_one_or_none(
            session=session, **filter_by
        )
        return user
