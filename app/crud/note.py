from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[
    Note,
    NoteCreate,
    NoteUpdate
]):
    async def get_by_user(
            self,
            user: int,
            session: AsyncSession,
    ):
        return (
            await session.execute(select(Note).where(
                Note.user_id == user.id
            ))
        ).scalars().all()


note_crud = CRUDNote(Note)
