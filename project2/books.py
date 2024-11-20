from fastapi import FastAPI, HTTPException, Path, Body, Query
from pydantic import BaseModel, Field
from typing import List, Dict

app = FastAPI(title="Books API", description="API for managing books")

class Book(BaseModel):
    id: int
    title: str = Field(min_length=1)
    author: str = Field(min_length=3)
    description: str = Field(min_length=10, max_length=100)
    published: bool = Field(default=False)

    def __str__(self):
        return f"Book(id={self.id}, title={self.title}, author={self.author}, description={self.description}, published={self.published})"

books: Dict[int, Book] = {}

def get_next_book_id():
    return max(books.keys(), default=0) + 1

def create_book(title: str, author: str, description: str, published: bool = False) -> Book:
    book = Book(
        id=get_next_book_id(),
        title=title,
        author=author,
        description=description,
        published=published
    )
    books[book.id] = book
    return book

# Initialize books
initial_books = [
    ("Nineteen Eighty-Four", "George Orwell", "A dystopian novel"),
    ("To Kill a Mockingbird", "Harper Lee", "A novel about the injustices of the American South"),
    ("Pride and Prejudice", "Jane Austen", "A novel about the injustices of the British society"),
    ("To the Lighthouse", "Virginia Woolf", "A novel about the injustices of the British society"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "A novel about the injustices of the American society")
]

for book_data in initial_books:
    create_book(*book_data, published=True)

@app.get("/books", status_code=200)
async def get_books():
    return list(books.values())

@app.get("/book/{id}", status_code=200)
async def get_book(id: int = Path(..., gt=0, description="The ID of the book to retrieve")):
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[id]

@app.get("/books/published", status_code=200)
async def get_published_books(published: bool = Query(..., description="Filter books by published status")):
    return [book for book in books.values() if book.published == published]

@app.post("/create-book", status_code=201)
async def create_book_endpoint(book: Book = Body(..., description="The book to create")):
    new_book = create_book(book.title, book.author, book.description, book.published)
    return new_book

@app.put("/update-book/{id}", status_code=204)
async def update_book(id: int = Path(..., gt=0, description="The ID of the book to update"), book: Book = Body(..., description="The book to update")):
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    book.id = id
    books[id] = book
    return book

@app.delete("/delete-book/{id}", status_code=204)
async def delete_book(id: int = Path(..., gt=0, description="The ID of the book to delete")):
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[id]
