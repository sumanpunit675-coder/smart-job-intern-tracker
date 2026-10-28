from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base
from app.models.user import User
from app.core.database import engine
from app.route.user import router as user_router

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"smart job/intern tracker API "}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
