from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session

from db.dbConnect import get_db
from typing import Optional,List
# from sqlalchemy.ext.asyncio import AsyncSession

from services.bookServices import book_service
from schemas.bookSchema import BookCreateModel,BookUpdateModel,Book
from auth.dependency import AccessTokenBearer,RollChecker

book_router=APIRouter(
    prefix="/api/v1/book",
    tags=["books"],
)
access_token_bearer= AccessTokenBearer()
role_checker = Depends( RollChecker(["admin","user"]))


# create Book
@book_router.post("/",response_model=Book, dependencies=[role_checker], status_code=status.HTTP_201_CREATED)
async def create_book(book_data:BookCreateModel,token_details=Depends(access_token_bearer),db:Session=Depends(get_db)):
    user_id = token_details.get("user")["user_uid"]
    return await book_service.create_a_book(book_data,user_id,db)

# get all books
@book_router.get("/",response_model=List[Book], dependencies=[role_checker], status_code=status.HTTP_200_OK)
async def get_books(db:Session=Depends(get_db),token_details=Depends(access_token_bearer)):
    return await book_service.get_all_books(db)

@book_router.get(
    "/user/{user_uid}", response_model=List[Book], dependencies=[role_checker], status_code=status.HTTP_200_OK
)
async def get_user_book_submissions(
    user_uid: str,
    db: Session = Depends(get_db),
    _: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_uid, db)
    return books


# get single books
@book_router.get("/{book_uid}",response_model=Book, dependencies=[role_checker], status_code=status.HTTP_200_OK)
async def get_book(book_uid:str,db:Session=Depends(get_db), token_details=Depends(access_token_bearer)):
    return await book_service.get_a_book(book_uid,db)

# update book
@book_router.patch("/{book_uid}",response_model=Book, dependencies=[role_checker], status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_uid:str,update_book_data:BookUpdateModel,db:Session=Depends(get_db), token_details=Depends(access_token_bearer)):
    return await book_service.update_book(book_uid,update_book_data,db)

# delete Book
@book_router.delete("/{book_uid}", dependencies=[role_checker], status_code=status.HTTP_202_ACCEPTED)
async def delete_book(book_uid:str,db:Session=Depends(get_db),token_details=Depends(access_token_bearer)):
    return await book_service.delete_a_book(book_uid,db)