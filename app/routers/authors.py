from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)

@router.get("/", response_model=list[schemas.Author])
def list_authors(db: Session = Depends(get_db)):
    return db.query(crud.models.Author).all()

@router.get("/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(crud.models.Author).filter(crud.models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, updated_author: schemas.AuthorCreate, db: Session = Depends(get_db)):
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
