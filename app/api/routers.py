from fastapi import APIRouter

from app.api.endpoints import note_router, user_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(note_router, prefix='/note', tags=['Note'])
