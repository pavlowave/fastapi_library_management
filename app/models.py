from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Author(Base):
    """
    Модель для таблицы "authors".
    Содержит информацию об авторах книг.
    """
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date)

    books = relationship("Book", back_populates="author")

class Book(Base):
    """
    Модель для таблицы "books".
    Содержит информацию о книгах, включая описание, автора и доступные копии.
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    available_copies = Column(Integer, default=1)

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", backref="book")

class Borrow(Base):
    """
    Модель для таблицы "borrows".
    Отображает информацию о выдаче книг читателям.
    """
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_name = Column(String, nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
