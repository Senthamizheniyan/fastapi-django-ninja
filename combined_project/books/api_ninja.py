from ninja import NinjaAPI, ModelSchema
from django.shortcuts import get_object_or_404
from .models import Book

api = NinjaAPI()

class BookSchema(ModelSchema):
    class Config:
        model = Book
        model_fields = ["id", "title", "author"]

class BookIn(ModelSchema):
    class Config:
        model = Book
        model_fields = ["title", "author"]

@api.get("/books", response=list[BookSchema])
def list_books(request):
    return Book.objects.all()

@api.get("/books/{book_id}", response=BookSchema)
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)

@api.post("/books", response=BookSchema)
def create_book(request, data: BookIn):
    book = Book.objects.create(**data.dict())
    return book

@api.put("/books/{book_id}", response=BookSchema)
def update_book(request, book_id: int, data: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in data.dict().items():
        setattr(book, attr, value)
    book.save()
    return book

@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}
