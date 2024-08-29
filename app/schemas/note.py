from typing import Optional

from pydantic import BaseModel, Field, field_validator


NULL_NAME = 'Название заметки не может быть пустым!'
NULL_DESCRIPTION = 'Описание заметки не может быть пустым!'


# Базовый класс схемы, от которого наследуем все остальные.
class NoteBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]

    class Config:
        extra = 'forbid'
        min_anystr_length = 1


class NoteCreate(NoteBase):
    name: str = Field(..., max_length=100)
    description: str


class NoteUpdate(NoteBase):
    @field_validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError(NULL_NAME)
        return value

    @field_validator('description')
    def description_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError(NULL_DESCRIPTION)
        return value


class NoteDB(NoteCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
