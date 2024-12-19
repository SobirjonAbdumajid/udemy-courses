from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2024)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "New book title",
                    "author": "New book author",
                    "description": "Book description",
                    "rating": 5,
                    "published_date": 2000
                }
            ]
        }
    )


BOOKS = [
    Book(1, "title 1", "author 1", "description 1", 5, 2010),
    Book(2, "title 2", "author 2", "description 2", 7, 2010),
    Book(3, "title 3", "author 3", "description 3", 5, 2000),
    Book(4, "title 4", "author 4", "description 4", 1, 2021),
    Book(5, "title 5", "author 5", "description 5", 6, 2019),
    Book(6, "title 6", "author 6", "description 6", 5, 2012),
]


@app.get("/books")
async def read_books():
    return BOOKS


@app.get('/books/{book_id}')
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get('/books/')
async def read_books_by_rating(rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return



# @app.post("/create_book")
# async def create_book(book_request=Body()):
#     BOOKS.append(book_request)


@app.post('/create-book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = BOOKS[-1].id + 1
    return book


@app.put('/books/update_book')
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete('/books/{book_id}')
async def delete_book(book_id: int = Path(gt=0, le=len(BOOKS))):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


@app.get('/books/published_date/')
async def get_book_by_published_data(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

