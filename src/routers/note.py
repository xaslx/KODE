from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.services.dependencies import get_note_service
from database import get_async_session
from typing import Annotated
from src.schemas.user import UserOut
from src.schemas.note import NoteAdd, NoteOut
from src.auth.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.note import NoteService
from exceptions import NotFoundException, NoteNotFoundException, NotAccessErrorException
from src.services.yandex_speller import check_text
from fastapi_versioning import version


note_router: APIRouter = APIRouter(prefix="/api/notes", tags=["Заметки"])


@note_router.get("", status_code=200)
@version(1)
async def get_all_my_notes(
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> list[NoteOut]:

    notes: list[NoteOut] = await note_service.get_all_notes(
        session=session, user_id=user.id
    )
    return notes


@note_router.get("/{note_id}", status_code=200)
@version(1)
async def get_my_note_by_id(
    note_id: int,
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> NoteOut | None:

    note: NoteOut = await note_service.get_note_by_id(session=session, note_id=note_id)
    if not note or note.user_id != user.id:
        raise NotFoundException
    return note


@note_router.post("", status_code=201)
@version(1)
async def create_new_note(
    note: NoteAdd,
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> NoteOut:


    checked_text: list[dict[str, str | int]] = await check_text(text=note.description)
    errors: list[str] = [word["word"] for word in checked_text]
    
    if errors:
        return JSONResponse(
            content={
                "Ошибка": f"Исправьте ошибки в следующих словах: {', '.join(errors)}"
            }
        )
    res: NoteOut = await note_service.add_new_note(
        session=session, **note.model_dump(), user_id=user.id
    )
    return res


@note_router.delete("/{note_id}", status_code=200)
@version(1)
async def delete_note(
    note_id: int,
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> None:

    note: NoteOut = await note_service.get_note_by_id(session=session, note_id=note_id)
    if not note:
        raise NoteNotFoundException
    if note.user_id != user.id:
        raise NotAccessErrorException
    return await note_service.delete_note(session=session, note_id=note_id)
