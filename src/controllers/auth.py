from schemas import UserRegisterSchema, UserLoginSchema
from db.models import User as UserModel, Bucket as BucketModel
from db.repository.user import query_user_by_email, add_user
from sqlalchemy.orm import Session
from fastapi import HTTPException
from helpers.auth import JwtAuthHelper

auth_helper = JwtAuthHelper()


def create_user(db: Session, user_data: UserRegisterSchema):
    """
    @Route: POST /api/v1/auth/register
    @Description: Register a new user
    @Args:
        db {Session} - Database session
        user_data {UserRegisterSchema} - User Registration data
    @Requires Auth: False
    """
    try:
        existing_user = query_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=400, detail="A user with this email already exists."
            )

        user = add_user(db, user_data)
        if user:
            return {
                "status": True,
                "message": "User successfully registered.",
                "data": user,
            }
        else:
            raise HTTPException(status_code=422, detail="User registration failed.")
    except Exception as e:
        print(e)
        raise HTTPException(detail=str(e), status_code=400)


def create_access_token(db: Session, email: str, password: str):
    """
    @Route: POST /api/v1/auth/login
    @Description: Create an access token to authenticate a user
    @Args:
        db {Session} - Database session
        email {str}  - User E-mail
        password {str} - User Password
    @Requires Auth: False
    """
    user = query_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=404, detail={"status": False, "message": "User does not exist."}
        )
    if not user.check_password(password):
        raise HTTPException(
            status_code=400,
            detail={"status": False, "message": "Password is incorrect."},
        )
    access_token = auth_helper.encode_jwt(user.id)
    return {
        "status": True,
        "message": "Login successful.",
        "data": user,
        "access_token": access_token,
    }
