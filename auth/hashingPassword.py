from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:

    # generating hash password
    def bcrypt_password(password:str):
        return pwd_context.hash(password)
    
    #veryfing hash passord
    def verify_password(plan_password:str,hash_password:str):
        return pwd_context.verify(plan_password,hash_password)
    
