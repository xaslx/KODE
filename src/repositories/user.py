from src.utils.repositories import SQLAlchemyRepository
from src.models.user import User


class UserRepository(SQLAlchemyRepository):
    model = User
