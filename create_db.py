from sqlmodel import SQLModel
from models import Book
from database import engine
print("creating db ...")

SQLModel.metadata.create_all(engine)