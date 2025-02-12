from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship

from typing import List,Optional
import uuid
from datetime import datetime,date

import sqlalchemy.dialects.postgresql as pg

from db.dbConnect import Base

# from .bookModel import Book


class User(Base):
    __tablename__="users"
    uid: uuid.UUID = Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash:str=Column(String, nullable= False)
    role : str = Column(pg.VARCHAR, nullable=False, server_default="user")
    is_verified:bool=Column(Boolean, default=False, nullable=False)
    created_at:datetime=Column(pg.TIMESTAMP, default=datetime.utcnow, nullable=False)
    update_at:datetime=Column(pg.TIMESTAMP,default=datetime.utcnow,onupdate=datetime.utcnow, nullable=False)

    books = relationship("Book", back_populates="user", lazy="selectin")
    # books: List["Book"] = relationship(
    #     back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    # def __repr__(self):
    #     return f"<User {self.username}>"