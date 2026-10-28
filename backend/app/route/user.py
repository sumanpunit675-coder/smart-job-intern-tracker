from fastapi import APIRouter, Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.models.user import User
from app.schema.user import UserCreate,userResponse,UserLogin,userUpdate
from app.core.security import hash_password,verify_password,create_access_token

from app.core.dependencies import get_current_user

router=APIRouter(prefix="/user",tags=["users"])

@router.post("/",response_model=userResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    hashed_password=hash_password(user.password)
    new_user=User(
        name=user.name,
        email=user.email,
        password=hashed_password
        )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
    return new_user

@router.post("/login")
def login_user(
    user_data:UserLogin,
    db:Session=Depends(get_db)
):
    existing_user=(db.query(User).filter(User.email==user_data.email)
                   .first())

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    is_password_correct=verify_password(user_data.password,existing_user.password)

    if not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token=create_access_token(user_id=existing_user.id)
    return{
        "message":"Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id":existing_user.id,
        "user_name":existing_user.name,
        "user_email":existing_user.email
    }


# this is for the testing purpose not used for the deployment
# @router.get("/auth-check")
# def auth_check(
#     current_user: User= Depends(get_current_user)
# ):
#     return {
#         "message": "Authentication successful",
#         "user_id": current_user.id,
#         "email": current_user.email
#     }

@router.get("/me",response_model=userResponse)
def get_current_user_info(
    current_user: User=Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=userResponse)
def update_my_profile(
    user_data: userUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_data.name is None and user_data.email is None:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    if user_data.email is not None:
        existing_user = db.query(User).filter(
            User.email == user_data.email,
            User.id != current_user.id
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already in use"
            )

    if user_data.name is not None:
        current_user.name = user_data.name

    if user_data.email is not None:
        current_user.email = user_data.email

    try:
        db.commit()
        db.refresh(current_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already in use"
        )

    return current_user

@router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    db.delete(current_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
