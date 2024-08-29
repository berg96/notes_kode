from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.core.db import Base


class Note(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
