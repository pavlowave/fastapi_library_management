import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_borrow_book_with_available_copies():
    response_author = client.post("/authors", json={"first_name": "Test", "last_name": "Author", "birth_date": "1985-05-15"})
    assert response_author.status_code == 200
    author_id = response_author.json()["id"]

    response_book = client.post("/books", json={"title": "Test Book", "description": "Description", "author_id": author_id, "available_copies": 3})
    assert response_book.status_code == 200
    book_id = response_book.json()["id"]

    response_borrow_1 = client.post("/borrows", json={"book_id": book_id, "reader_name": "Reader 1", "borrow_date": "2024-12-11", "return_date": "2024-12-12"})
    assert response_borrow_1.status_code == 200
    assert response_borrow_1.json()["reader_name"] == "Reader 1"

    response_borrow_2 = client.post("/borrows", json={"book_id": book_id, "reader_name": "Reader 2", "borrow_date": "2024-12-12", "return_date": "2024-12-13"})
    assert response_borrow_2.status_code == 200
    assert response_borrow_2.json()["reader_name"] == "Reader 2"

    response_book_after_borrows = client.get(f"/books/{book_id}")
    assert response_book_after_borrows.status_code == 200
    assert response_book_after_borrows.json()["available_copies"] == 1

def test_borrow_unavailable_book():
    response_author = client.post("/authors", json={"first_name": "Test", "last_name": "Author", "birth_date": "1985-05-15"})
    assert response_author.status_code == 200
    author_id = response_author.json()["id"]

    response_book = client.post("/books", json={"title": "Test Book Unavailable", "description": "Description", "author_id": author_id, "available_copies": 0})
    assert response_book.status_code == 200
    book_id = response_book.json()["id"]

    response_borrow = client.post("/borrows", json={"book_id": book_id, "reader_name": "Reader 3", "borrow_date": "2024-12-12", "return_date": "2024-12-13"})
    assert response_borrow.status_code == 400
    assert response_borrow.json()["detail"] == "No available copies"
