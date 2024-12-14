from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
import logging
from app import models

logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Borrow)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_borrow(db, borrow)
    except ValueError as e:
        logger.error("Error creating borrow", exc_info=e)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[schemas.Borrow])
def list_borrows(db: Session = Depends(get_db)):
    return db.query(crud.models.Borrow).all()

@router.get("/{borrow_id}", response_model=schemas.Borrow)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(crud.models.Borrow).filter(crud.models.Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

@router.patch("/{borrow_id}/return", response_model=schemas.Borrow)
def return_borrow(borrow_id: int, return_date: schemas.BorrowReturn, db: Session = Depends(get_db)):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if not borrow:
        logger.error(f"Borrow with ID {borrow_id} not found.")
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
