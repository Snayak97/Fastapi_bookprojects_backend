from fastapi import APIRouter,Depends,HTTPException,status,Response
from fastapi.responses import JSONResponse

from db.dbConnect import get_db
from typing import Optional,List
from sqlalchemy.orm import Session

from schemas.userSchema import CreateUserModel,UserLoginModel,UserModel,UserBooksModel

from services.userService import user_service
from auth.hashingPassword import Hash

from auth.tokns import Token
from datetime import timedelta, datetime
from config import Config

from auth.dependency import RefreshTokenBearer,AccessTokenBearer,get_current_user, RollChecker
role_checker = RollChecker(["admin","user"])

from db.redis import add_jwt_id_to_blocklist





user_router=APIRouter(
    prefix="/api/v1/user",
    tags=["users"],
)

@user_router.post("/signup",response_model = UserModel)
async def create_user_account(user_data:CreateUserModel,db:Session=Depends(get_db)):
    email=user_data.email
    exist_user= await user_service.user_exists(email,db)
    if exist_user:
        raise HTTPException(
        status_code= status.HTTP_403_FORBIDDEN, detail= "user Exist"
    )
    new_user= await user_service.create_user(user_data,db)
    return new_user

@user_router.post("/login")
async def login_user(login_data:UserLoginModel, db:Session=Depends(get_db)):
    email= login_data.email
    password= login_data.password
    user= await user_service.get_user_by_email(email,db)

    if user is not None:
        password_valid= Hash.verify_password(password,user.password_hash)
        if password_valid:
            access_token= Token.create_acess_token(
                user_data={
                    "email" : user.email,
                    "user_uid": str(user.uid),
                }
            )
            refresh_token=Token.create_acess_token(
                user_data={
                    "email" : user.email,
                    "user_uid": str(user.uid),
                },
                refresh=True,
                expiry= timedelta(days=Config.REFRESS_TOKEN_EXPIRE_DAYS)
            )
            return JSONResponse(
                 content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    # "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
    raise HTTPException(
        status_code=403, detail= "invalid email or password"
    )

@user_router.get("/refresh_token")
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token= Token.create_acess_token(
            user_data= token_details["user"]
        )
        return JSONResponse(
            content={
                "access_token" : new_access_token
            }
       )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail= "invalid  or Expairy token"
    )
     


@user_router.get("/get_current_user",response_model= UserBooksModel)
async def get_current_user(
    user = Depends(get_current_user),
    _:bool = Depends(role_checker)
):
    return user

@user_router.get("/logout")
async def revoke_token(toke_details : dict = Depends(AccessTokenBearer())):
# async def revoke_token():
#     # print(r.ping())

    jwt_id = toke_details["jwt_id"]

    await add_jwt_id_to_blocklist(jwt_id)
    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )