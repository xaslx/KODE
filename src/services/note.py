from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.note import NoteOut
from src.repositories.note import NoteRepository


class NoteService:

    def __init__(self, note_repository: type[NoteRepository]) -> None:
        self.note_repository = note_repository()

    async def add_new_note(self, session: AsyncSession, **data) -> NoteOut:
        new_note: NoteOut = await self.note_repository.add(session=session, **data)
        return new_note

    async def get_note_by_id(self, session: AsyncSession, note_id: int) -> NoteOut:
        note: NoteOut = await self.note_repository.find_one_or_none(
            session=session, id=note_id
        )
        return note

    async def get_all_notes(self, session: AsyncSession, **filter_by) -> list[NoteOut]:
        note: NoteOut = await self.note_repository.find_all(
            session=session, **filter_by
        )
        return note

    async def delete_note(self, session: AsyncSession, note_id: int) -> None:
        await self.note_repository.delete(session=session, id=note_id)
