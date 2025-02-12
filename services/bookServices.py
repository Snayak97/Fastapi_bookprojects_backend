from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session
from datetime import datetime
from models import Book

from sqlalchemy.future import select
from sqlalchemy import desc

import uuid

from schemas.bookSchema import BookCreateModel,BookUpdateModel
class BookService:
    
    async def get_all_books(self,db:AsyncSession):
        # Anotheraproch by asending
        # books=db.query(Book).all()

        #using desending
        statement = select(Book).order_by(desc(Book.created_at))
        # Execute the statement and await the result
        result =db.execute(statement)
        # Extract the list of books
        books = result.scalars().all()
        return books
    
    async def get_user_books(self, user_uid: str, db: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        result =db.execute(statement)
        books = result.scalars().all()
        return books
    
    
    async def get_a_book(self,book_uid,db:AsyncSession):
        try:
        # Ensure the book_uid is a UUID object
            book_uid = uuid.UUID(book_uid)
        except ValueError:
            return f"Invalid UUID format: {book_uid}"
       
        # another approch
        # statement = select(Book).filter(Book.uid == book_uid)
        # book = db.scalars(statement).first() 
       
        book= db.query(Book).filter(Book.uid==book_uid).first()
        return book
        

    async def create_a_book(self,book_data, user_id:str ,db:AsyncSession):
        book_data_dict=book_data.model_dump()
        print(book_data_dict)
        new_book=Book(**book_data_dict)
       
        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )
        new_book.user_uid= user_id
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    
    async def update_book(self,book_uid,update_book_data:BookUpdateModel,db:AsyncSession):
        book_to_update=db.query(Book).filter(Book.uid==book_uid).first()
        # book_to_update = await self.get_a_book(book_uid, db)
        print(book_to_update)
        if book_to_update is not None:
            book_data_dict=update_book_data.model_dump()
            print(book_data_dict)
            for key,val in book_data_dict.items():
                setattr(book_to_update,key,val)
            db.commit()
            return book_to_update
        else:
            return None


    async def delete_a_book(self,book_uid,db:AsyncSession):
        book_to_delete= db.query(Book).filter(Book.uid==book_uid).first()

        if book_to_delete is not None:
            db.delete(book_to_delete)
            db.commit()
            return "Book deleted"
        else:
            return None
        
    
   
book_service=BookService()

