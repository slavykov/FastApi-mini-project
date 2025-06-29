from typing import Union, Any
from fastapi import FastAPI
from BookModel import Book_Model

app = FastAPI()

books = []


@app.get("/books",
         tags=["Книги"],
         summary="Получить все книги")
def get_books():
    return books


@app.post("/books",
          tags=["Книги"],
          summary="Добавить книгу"
          )
def add_book(Book: Book_Model):
    books.append(
        {"id": len(books) + 1,
         "title": Book.title,
         "author": Book.author
         }
    )
    return {"success": True, "message": "Книга успешно добавлена"}


@app.put("/books/{book_id}",
        tags=["Книги"],
        summary="Редактировать книгу"
         )
def update_item(book_id: int, Book: Book_Model):
   return {"book_title": Book.title, "book_id": book_id}
