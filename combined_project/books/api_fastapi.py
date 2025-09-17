import os
import django
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ensure Django settings are available before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "combined_project.settings")
django.setup()

from .models import Book  # now safe to import

app = FastAPI(title="Books FastAPI (uses Django ORM)")

# CORS to allow requests from the Django frontend (served at 127.0.0.1:8000)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookSchema(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True

class BookIn(BaseModel):
    title: str
    author: str

@app.get("/books", response_model=list[BookSchema])
def list_books():
    return list(Book.objects.all())

@app.get("/books/{book_id}", response_model=BookSchema)
def get_book(book_id: int):
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=BookSchema)
def create_book(data: BookIn):
    book = Book.objects.create(**data.dict())
    return book

@app.put("/books/{book_id}", response_model=BookSchema)
def update_book(book_id: int, data: BookIn):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = data.title
    book.author = data.author
    book.save()
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    book.delete()
    return {"success": True}
