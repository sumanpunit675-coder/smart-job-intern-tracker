from sqlalchemy import Column, Integer,String,Text,ForeignKey
from app.core.database import Base

class job(Base):
    __tablename__="jobs"

    id=Column(Integer,primary_key=True,index=True)
    company=Column(String(100),nullable=False)
    role=Column(String(100),nullable=False)
    location=Column(String(100),nullable=False)
    job_type = Column(String(50), nullable=False)
    salary = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    job_url = Column(String(500), nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )