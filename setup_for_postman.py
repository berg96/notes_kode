import asyncio
import contextlib
from fastapi import Depends
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import EmailStr
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.user import UserManager
from app.models import User
from app.schemas.user import UserCreate

DATABASE_URL = 'postgresql+asyncpg://user:password@localhost:5432/notes_kode_db'

engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def reset_database():
    """Сброс схемы базы данных."""
    async with engine.begin() as conn:
        def sync_operations(sync_conn):
            metadata.reflect(bind=sync_conn)
            metadata.drop_all(bind=sync_conn)
            metadata.create_all(bind=sync_conn)

        await conn.run_sync(sync_operations)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr, password: str, is_superuser: bool = False
):
    """Создание пользователя."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        print(f'Пользователь с email {email} уже существует.')


async def main():
    """Основная функция: сброс базы данных и создание суперпользователя."""
    try:
        await reset_database()
        await create_user('root@admin.ru', 'root', is_superuser=True)
        print('База данных успешно сброшена и создан суперпользователь для тестов!')
    except SQLAlchemyError as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    asyncio.run(main())