from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
import logging
from app import models

router = APIRouter()

def get_db():
    """
    Создает сессию базы данных для обработки запросов.
    Автоматически закрывает сессию после выполнения.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Borrow)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    """
    Создает запись о выдаче книги.
    :param borrow: Данные о выдаче книги (Pydantic-модель BorrowCreate).
    :param db: Сессия базы данных.
    :return: Созданная запись о выдаче книги (Pydantic-модель Borrow).
    :raises HTTPException: Если недоступны копии книги для выдачи.
    """
    try:
        return crud.create_borrow(db, borrow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[schemas.Borrow])
def list_borrows(db: Session = Depends(get_db)):
    """
    Возвращает список всех записей о выдаче книг.
    :param db: Сессия базы данных.
    :return: Список записей о выдаче (Pydantic-модель Borrow).
    """
    return db.query(crud.models.Borrow).all()

@router.get("/{borrow_id}", response_model=schemas.Borrow)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о выдаче книги по её ID.
    :param borrow_id: Идентификатор выдачи.
    :param db: Сессия базы данных.
    :return: Данные о выдаче книги (Pydantic-модель Borrow).
    :raises HTTPException: Если запись о выдаче не найдена.
    """
    borrow = db.query(crud.models.Borrow).filter(crud.models.Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

@router.patch("/{borrow_id}/return", response_model=schemas.Borrow)
def return_borrow(borrow_id: int, return_date: schemas.BorrowReturn, db: Session = Depends(get_db)):
    """
    Обрабатывает возврат книги.
    :param borrow_id: Идентификатор записи о выдаче книги.
    :param return_date: Дата возврата (Pydantic-модель BorrowReturn).
    :param db: Сессия базы данных.
    :return: Обновленная запись о выдаче книги с датой возврата.
    :raises HTTPException: Если запись о выдаче не найдена или книга уже возвращена.
    """
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")

    if borrow.return_date:
        borrow.return_date = return_date.return_date
        db.commit()
        db.refresh(borrow)
        book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()

        if book:
            book.available_copies += 1
            db.commit()
            db.refresh(book)
        raise HTTPException(status_code=400, detail="Borrow already returned")
    
    return borrow
