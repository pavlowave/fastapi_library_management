from fastapi import FastAPI
from app.database import Base, engine
from app.routers import authors, books, borrows
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Library API Docs")

@app.get("/redoc", include_in_schema=False)
def redoc_ui_html():
    return get_redoc_html(openapi_url="/openapi.json", title="Library API Docs")


app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(borrows.router, prefix="/borrows", tags=["Borrows"])
