from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    """
    Создает сессию базы данных для работы с запросами.
    Сессия автоматически закрывается после выполнения запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Создает новую книгу.
    :param book: Данные новой книги (Pydantic-модель BookCreate).
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Созданная книга (Pydantic-модель Book).
    """
    return crud.create_book(db, book)

@router.get("/", response_model=list[schemas.Book])
def list_books(db: Session = Depends(get_db)):
    """
    Возвращает список всех книг из базы данных.
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Список книг (Pydantic-модель Book).
    """
    return db.query(crud.models.Book).all()

@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о книге по её ID.
    :param book_id: Идентификатор книги.
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Данные книги (Pydantic-модель Book).
    :raises HTTPException: Если книга с указанным ID не найдена.
    """
    book = db.query(crud.models.Book).filter(crud.models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о книге по её ID.
    :param book_id: Идентификатор книги.
    :param updated_book: Обновленные данные книги (Pydantic-модель BookCreate).
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Обновленная книга (Pydantic-модель Book).
    :raises HTTPException: Если книга с указанным ID не найдена.
    """
    book = db.query(crud.models.Book).filter(crud.models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Удаляет книгу и связанные записи о выдаче.
    :param book_id: Идентификатор книги.
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Сообщение об успешном удалении.
    :raises HTTPException: Если книга с указанным ID не найдена.
    """
    book = db.query(crud.models.Book).filter(crud.models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.query(crud.models.Borrow).filter(crud.models.Borrow.book_id == book_id).delete()

    db.delete(book)
    db.commit()


    return {"message": "Book and associated borrow records deleted successfully"}
