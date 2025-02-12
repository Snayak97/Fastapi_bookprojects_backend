from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import desc

import uuid

from datetime import datetime
from models import User
from auth.hashingPassword import Hash

from schemas.userSchema import CreateUserModel


class UserService:
    
    async def get_user_by_email(self,email,db:AsyncSession):
        user= db.query(User).filter(User.email==email).first()
        # statement = select(User).where(User.email==email)
        # result = db.execute(statement)
        # user=result.scalars().first()
        return user

    async def user_exists(self,email,db:AsyncSession):
        exist_user = await self.get_user_by_email(email,db)
        return True if exist_user is not None else False

    async def create_user(self,user_data:CreateUserModel,db:AsyncSession):
        user_data_dict= user_data.model_dump()
        new_user= User(** user_data_dict)
        new_user.password_hash = Hash.bcrypt_password(user_data_dict["password_hash"])
        new_user.role = "user"
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

        
    async def delete_user(self,user_data,db:AsyncSession):
        pass


user_service=UserService()