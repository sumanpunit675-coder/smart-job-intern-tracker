from pydantic import BaseModel,Field,ConfigDict

class jobCreate(BaseModel):
    company: str=Field(min_length=2,max_length=100)
    role: str=Field(min_length=2,max_length=100)
    location: str=Field(min_length=2,max_length=100)
    job_type: str=Field(min_length=3,max_length=50)

    salary:str|None=None
    description:str|None=None
    job_url: str| None=None


class jobResponse(BaseModel):
    id:int
    company:str
    role:str
    location:str
    job_type:str
    salary:str|None=None
    description:str|None=None
    user_id:int

class Config:
    from_attributes = True

