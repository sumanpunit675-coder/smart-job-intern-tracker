import re
from pydantic import BaseModel,EmailStr,Field,field_validator

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str: #cls class ko as a parameter ke rup me dal raha hai or ye batane ke liye upper @Classmethod likha hai yaha class hai userCreate wala
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).+$"
        if not re.match(pattern, v):# re generally regular exp hai jo text ke under regular pattern find karne ke liye use kiya jata hai
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character")
        return v
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class userUpdate(BaseModel):
    name:str|None=None
    email: EmailStr |None=None
class userResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True
