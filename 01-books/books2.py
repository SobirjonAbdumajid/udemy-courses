from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

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


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "New book title",
                    "author": "New book author",
                    "description": "Book description",
                    "rating": 5
                }
            ]
        }
    )


BOOKS = [
    Book(1, "title 1", "author 1", "description 1", 5),
    Book(2, "title 2", "author 2", "description 2", 7),
    Book(3, "title 3", "author 3", "description 3", 5),
    Book(4, "title 4", "author 4", "description 4", 1),
    Book(5, "title 5", "author 5", "description 5", 6),
    Book(6, "title 6", "author 6", "description 6", 5),
]


@app.get("/books")
async def read_books():
    return BOOKS


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
