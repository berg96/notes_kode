from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_yandex_spelling
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.note import note_crud
from app.models import User

from app.schemas.note import NoteDB, NoteCreate

router = APIRouter()


@router.get(
    '/',
    response_model=list[NoteDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_notes(
    session: AsyncSession = Depends(get_async_session),
):
    """Вывод списка всех заметок пользователей (только для суперюзеров)."""
    return await note_crud.get_multi(session)


@router.post(
    '/',
    response_model=NoteDB,
)
async def create_new_note(
    note: NoteCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await check_yandex_spelling(note.name)
    await check_yandex_spelling(note.description)
    return await note_crud.create(note, session, user)


@router.get(
    '/my',
    response_model=list[NoteDB],
)
async def get_my_notes(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех заметок для текущего пользователя."""
    return await note_crud.get_by_user(user, session)
