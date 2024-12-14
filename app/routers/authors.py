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

@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """
    Создает нового автора.
    :param author: Данные нового автора (Pydantic-модель AuthorCreate).
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Созданный автор (Pydantic-модель Author).
    """
    return crud.create_author(db, author)

@router.get("/", response_model=list[schemas.Author])
def list_authors(db: Session = Depends(get_db)):
    """
    Возвращает список всех авторов из базы данных.
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Список авторов (Pydantic-модель Author).
    """
    return db.query(crud.models.Author).all()

@router.get("/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Возвращает автора по его ID.
    :param author_id: Идентификатор автора.
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Данные автора (Pydantic-модель Author).
    :raises HTTPException: Если автор с указанным ID не найден.
    """
    author = db.query(crud.models.Author).filter(crud.models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, updated_author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """
    Обновляет данные автора по его ID.
    :param author_id: Идентификатор автора.
    :param updated_author: Обновленные данные автора (Pydantic-модель AuthorCreate).
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Обновленный автор (Pydantic-модель Author).
    :raises HTTPException: Если автор с указанным ID не найден.
    """
    author = db.query(crud.models.Author).filter(crud.models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in updated_author.dict().items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author

@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Удаляет автора, а также связанные книги и записи о выдаче.
    :param author_id: Идентификатор автора.
    :param db: Сессия базы данных (генерируется автоматически).
    :return: Сообщение об успешном удалении.
    :raises HTTPException: Если автор с указанным ID не найден.
    """
    author = db.query(crud.models.Author).filter(crud.models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    borrows = db.query(crud.models.Borrow).filter(crud.models.Borrow.book_id.in_(db.query(crud.models.Book.id).filter(crud.models.Book.author_id == author_id))).all()
    for borrow in borrows:
        db.delete(borrow)

    books = db.query(crud.models.Book).filter(crud.models.Book.author_id == author_id).all()
    for book in books:
        db.delete(book)

    db.delete(author)
    db.commit()
    return {"message": "Author and related books and borrow records deleted successfully"}
