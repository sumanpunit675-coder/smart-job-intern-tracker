from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import settings

password_hash=PasswordHash.recommended()

def hash_password(password: str)->str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str)->bool:
    return password_hash.verify(password,hashed_password)

def create_access_token(user_id:int)->str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                                                )# timedelta represent the time duration i.e curr time + time duration
    payload={
        "sub":str(user_id),
        "exp":expire
    }
    token=jwt.encode(
        payload,settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
        )
    return token
def verify_access_token(token:str):
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,
                           algorithms=[settings.ALGORITHM]
                           )
        user_id=payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except(jwt.InvalidTokenError,ValueError):
        return None