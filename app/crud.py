from sqlalchemy.orm import Session
from app import models, schemas

def create_author(db: Session, author: schemas.AuthorCreate):
    """
    Создание нового автора в базе данных.
    :param db: Сессия базы данных.
    :param author: Pydantic-модель AuthorCreate с данными автора.
    :return: Созданная запись автора (объект модели Author).
    """
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def create_book(db: Session, book: schemas.BookCreate):
    """
    Создание новой книги в базе данных.
    :param db: Сессия базы данных.
    :param book: Pydantic-модель BookCreate с данными книги.
    :return: Созданная запись книги (объект модели Book).
    """
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_borrow(db: Session, borrow: schemas.BorrowCreate):
    """
    Создание записи о выдаче книги.
    :param db: Сессия базы данных.
    :param borrow: Pydantic-модель BorrowCreate с данными о выдаче.
    :return: Созданная запись о выдаче (объект модели Borrow).
    :raises ValueError: Если нет доступных копий книги.
    """
    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if book and book.available_copies > 0:
        book.available_copies -= 1
        db_borrow = models.Borrow(**borrow.dict())
        db.add(db_borrow)
        db.commit()
        db.refresh(db_borrow)
        return db_borrow
    raise ValueError("No available copies")
