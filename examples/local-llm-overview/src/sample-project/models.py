"""도서 데이터 모델"""

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str | None = None
    category: str = "일반"


class Book(BookCreate):
    id: int
