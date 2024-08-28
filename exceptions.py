from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseException):
    status_code = 409
    detail = "Пользователь уже существует"


class IncorrectUsernameOrPasswordException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class UserNotFoundException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь не найден"


class NotAccessErrorException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Недостаточно прав"


class UnauthorizedUserException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не вошли в систему"


class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class NotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Страница не найдена"


class NoteNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Заметка не найдена"
