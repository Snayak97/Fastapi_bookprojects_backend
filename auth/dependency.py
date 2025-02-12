from fastapi.security import HTTPBearer
from fastapi import Depends, Request, status ,HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import Any, List,Optional   

from auth.tokns import Token
from db.redis import token_in_blocklist

from db.dbConnect import get_db
from models import User
from services.userService import user_service



class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        # print(creds.scheme) # return bereer
        # print(creds.credentials) # return token
        token = creds.credentials
        token_data = Token.decoded_token(token)

        if not self.token_valid(token):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"error" : "this token is invalid or expiry",
            "resoulation": "pls get new token"   }  )
        
        if await token_in_blocklist(token_data["jwt_id"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"error" : "this token is invalid or revoked",
            "resulation": "pls get new token"   }  )


        self.verify_token_data(token_data)
        
        return token_data


    def token_valid(self,token:str)->bool:
        token_data = Token.decoded_token(token)
        return token_data is not None
           
    
    def verify_token_data(self, token_data):
        raise HTTPException(status_code=403,detail="Please Override this method in child classes") 


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="please provide Acess Token token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="please provide Refresh Token token")


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    db: Session = Depends(get_db),
    ):
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, db)

    return user


class RollChecker:
    def __init__(self,allowed_roles : List[str])->None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user : User = Depends(get_current_user)) ->Any:
        # if not current_user.is_verified:
        #     raise HTTPException
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You r not permited to perform this action"
        )