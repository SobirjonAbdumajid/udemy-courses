from fastapi import FastAPI, Body

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, "title 1", "author 1", "description 1", 5),
    Book(1, "title 2", "author 2", "description 2", 7),
    Book(1, "title 3", "author 3", "description 3", 5),
    Book(1, "title 4", "author 4", "description 4", 1),
    Book(1, "title 5", "author 5", "description 5", 6),
    Book(1, "title 6", "author 6", "description 6", 5),
]


@app.get("/books")
async def read_books():
    return BOOKS


@app.post("/create_book")
async def create_book(book_request=Body()):
    BOOKS.append(book_request)

