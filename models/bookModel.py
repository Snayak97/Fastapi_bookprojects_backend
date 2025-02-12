from sqlalchemy import Column, Integer, String,ForeignKey,Date,DateTime
from sqlalchemy.orm import relationship



from typing import List,Optional
import uuid
from datetime import date,datetime

import sqlalchemy.dialects.postgresql as pg

from db.dbConnect import Base

# from models import User



class Book(Base):
    __tablename__="books"
    uid: uuid.UUID = Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    page_count = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    user_uid: Optional[uuid.UUID] = Column(pg.UUID(as_uuid=True), ForeignKey("users.uid"),nullable=True)
    created_at:datetime=Column(pg.TIMESTAMP, default=datetime.utcnow, nullable=False)
    update_at:datetime=Column(pg.TIMESTAMP,default=datetime.utcnow,onupdate=datetime.utcnow, nullable=False)
    

    user = relationship("User", back_populates="books")
    # user: Optional[User] = relationship(back_populates="books")




# class Book(Base):
#     __tablename__ = "books"

#     # Columns
#     uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
#     title = Column(String, nullable=False)
#     author = Column(String, nullable=False)
#     publisher = Column(String, nullable=False)
#     published_date = Column(Date, nullable=False)
#     page_count = Column(Integer, nullable=False)
#     language = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
