from contextlib import asynccontextmanager
from typing import Union, Any, Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session, select, create_engine

from BookModel import Book_Model


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/books",
         tags=["Книги"],
         summary="Получить все книги")
def get_books(session:SessionDep, offset: int=0, limit: Annotated[int, Query(le=100)]=100,)->list[Book_Model]:
    books = session.exec(select(Book_Model).offset(offset).limit(limit)).all()
    return books



@app.post("/books",
          tags=["Книги"],
          summary="Добавить книгу"
          )
def add_book(Book: Book_Model, session: SessionDep)->Book_Model:
    session.add(Book)
    session.commit()
    session.refresh(Book)
    return {"success": True, "message": "Книга успешно добавлена"}


@app.delete("/books/{book_id}",
            tags=["Книги"],
            summary="Удалить книгу")
def delete_book(book_id:int, session:SessionDep):
    book = session.get(Book_Model, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(book)
    session.commit()
    return {"ok":True}