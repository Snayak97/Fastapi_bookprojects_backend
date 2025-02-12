import jwt
import logging
import uuid
from datetime import datetime,timedelta,timezone

from config import Config



class Tokens:

    def create_acess_token(self, user_data:dict, expiry:timedelta | None = None, refresh:bool=False):
        payload={}
        
        payload["user"] = user_data
        payload["exp"] = datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(minutes = Config.ACCESS_TOKEN_EXPIRE_MINUTES) )
        payload["jwt_id"] = str(uuid.uuid4())
        payload["refresh"] = refresh

        token = jwt.encode(
            payload = payload,
            key = Config.JWT_SECRET_KEY,
            algorithm = Config.JWT_ALGORITHM
        )
        return token
    
    def decoded_token(self,token:str)->dict:
        try:
            token_data= jwt.decode(
            jwt=token,
            key = Config.JWT_SECRET_KEY,
            algorithms = [Config.JWT_ALGORITHM]
            )
            return token_data
        except jwt.PyJWTError as e:
            logging.exception(e)
            return None


Token=Tokens()
