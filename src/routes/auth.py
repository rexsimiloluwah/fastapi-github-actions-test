from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from controllers import auth as auth_controller
from dependency import get_db
from schemas import (
    UserRegisterSchema,
    UserLoginSchema,
)

# User Router
router = APIRouter()

@router.post("/auth/register",response_model=dict)
def register(user_data:UserRegisterSchema,db:Session=Depends(get_db)):
    return auth_controller.create_user(db,user_data)
    

@router.post("/auth/login",response_model=dict)
def login(user_data:UserLoginSchema,db:Session=Depends(get_db)):
    return auth_controller.create_access_token(db,user_data.email,user_data.password)
