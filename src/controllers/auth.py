from schemas import UserRegisterSchema, UserLoginSchema
from models import User as UserModel, Bucket as BucketModel
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
        existing_user = db.query(UserModel).filter_by(email=user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="A user with this email already exists."
            )
        user = UserModel(
            email=user_data.email,
            username=user_data.username,
            bio=user_data.bio,
            location=user_data.location,
            phone_number=user_data.phone_number,
            website=user_data.website,
        )
        user.set_password(user_data.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "status": True,
            "message": "User successfully registered.",
            "data": user,
        }
    except Exception as e:
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
    user = db.query(UserModel).filter_by(email=email).first()
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
