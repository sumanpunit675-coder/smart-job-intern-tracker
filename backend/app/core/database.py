from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine=create_engine(settings.DATABASE_URL,
                     connect_args={} # it is used for providing extra features to the database driver here pymysql
                     )

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db=SessionLocal()
    
    try:
        yield db # yield:-it is used to give access of session to the endpoint of fastapi temprorarily.
    finally:
        db.close()