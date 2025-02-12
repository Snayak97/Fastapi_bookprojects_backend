import uuid

from pydantic import BaseModel
from datetime import datetime,date

from typing import List,Optional

class Book(BaseModel):
    uid: uuid.UUID   
    title : str
    author :str
    publisher : str
    published_date : date
    page_count : int
    language : str
    created_at:datetime
    update_at:datetime
    # class Config():
    #     from_attributes =True

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    # class Config():
    #     from_attributes =True

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str