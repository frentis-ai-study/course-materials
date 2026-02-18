"""사내 도서 관리 API — OpenCode 데모용 샘플 프로젝트"""

from fastapi import FastAPI, HTTPException
from models import Book, BookCreate

app = FastAPI(title="사내 도서 관리 API", version="0.1.0")

# 간단한 인메모리 저장소
books: dict[int, Book] = {}
next_id = 1


@app.get("/books", response_model=list[Book])
def list_books():
    """등록된 모든 도서 조회"""
    return list(books.values())


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """특정 도서 조회"""
    if book_id not in books:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")
    return books[book_id]


@app.post("/books", response_model=Book, status_code=201)
def create_book(book: BookCreate):
    """새 도서 등록"""
    global next_id
    new_book = Book(id=next_id, **book.model_dump())
    books[next_id] = new_book
    next_id += 1
    return new_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """도서 삭제"""
    if book_id not in books:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")
    del books[book_id]
