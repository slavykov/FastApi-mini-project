from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Book_Model(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
