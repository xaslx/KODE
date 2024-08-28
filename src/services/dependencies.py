from src.repositories.user import UserRepository
from src.services.user import UserService

from src.repositories.note import NoteRepository
from src.services.note import NoteService


def get_user_service():
    return UserService(UserRepository)


def get_note_service():
    return NoteService(NoteRepository)
