from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Bookstore"}

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}

@app.get("/books/")
async def read_book_by_category(category: str):
    return [book for book in BOOKS if book['category'].casefold() == category.casefold()]

@app.get("/books/by_author/{book_author}")
async def read_book_autohor(book_author: str):
    return [book for book in BOOKS if book['author'].casefold() == book_author.casefold()]


@app.get("/books/{book_author}/")
async def read_book_by_author(author: str, category: str):
    return [book for book in BOOKS if book['author'].casefold() == author.casefold() and book['category'].casefold() == category.casefold()]

@app.post("/books/create_book")
async def create_book(book: dict = Body(...)):
    BOOKS.append(book)
    return book

@app.put("/books/update_book")
async def update_book(book: dict = Body(...)):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book['title'].casefold():
            BOOKS[i] = book
    return book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}

