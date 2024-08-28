from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete


class AbstractRepository(ABC):

    @abstractmethod
    async def add():
        pass

    @abstractmethod
    async def find_one_or_none():
        pass

    @abstractmethod
    async def find_all():
        pass

    @abstractmethod
    async def delete():
        pass


class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def add(self, session: AsyncSession, **data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()

    async def find_one_or_none(self, session: AsyncSession, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all(self, session: AsyncSession, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await session.execute(stmt)
        return res.scalars().all()

    async def delete(self, session: AsyncSession, id: int) -> None:
        stmt = delete(self.model).filter_by(id=id)
        await session.execute(stmt)
        await session.commit()
