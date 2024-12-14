from sqlalchemy.orm import Session
from app import models, schemas

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_borrow(db: Session, borrow: schemas.BorrowCreate):
    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if book and book.available_copies > 0:
        book.available_copies -= 1
        db_borrow = models.Borrow(**borrow.dict())
        db.add(db_borrow)
        db.commit()
        db.refresh(db_borrow)
        return db_borrow
    raise ValueError("No available copies")
