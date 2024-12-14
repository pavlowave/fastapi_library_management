from pydantic import BaseModel
from datetime import date
from pydantic import Field
from typing import Optional

class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    description: str
    author_id: int
    available_copies: int = Field(default=1, ge=0)

    class Config:
        orm_mode = True

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class BorrowBase(BaseModel):
    book_id: int
    reader_name: str
    borrow_date: date
    return_date: Optional[date] = None

class BorrowCreate(BorrowBase):
    pass

class Borrow(BorrowBase):
    id: int
    return_date: date

    class Config:
        orm_mode = True


class BorrowReturn(BaseModel):
    return_date: date
