from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base

class User(Base):
    __tablename__="users"
    
    id:Mapped[int] =mapped_column(primary_key=True,index=True)# if you set the primary key to sqlalchemy then autoincrement property is auto applied to it.
    
    name: Mapped[str]=mapped_column(String(50),nullable=False)
    
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    
    password: Mapped[str]=mapped_column(String(255))