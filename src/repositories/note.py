from src.utils.repositories import SQLAlchemyRepository
from src.models.note import Note


class NoteRepository(SQLAlchemyRepository):
    model = Note
