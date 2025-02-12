from pydantic import BaseModel, constr
import uuid
from datetime import datetime,date

from typing import List,Optional
from schemas.bookSchema import Book

class CreateUserModel(BaseModel):
    first_name: constr(max_length=25)  # String with max length of 25
    last_name: constr(max_length=25)   # String with max length of 25
    username: constr(max_length=20)     # String with max length of 8
    email: constr(max_length=40)       # String with max length of 40
    password_hash: constr(min_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str 
    created_at: datetime
    update_at: datetime

class UserBooksModel(UserModel):
    books: List[Book]

class UserLoginModel(BaseModel):
    email: str = constr(max_length=40)
    password: str = constr(min_length=6)