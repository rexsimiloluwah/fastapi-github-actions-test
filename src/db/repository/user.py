from typing import Any
from sqlalchemy.orm import Session
from schemas import UserRegisterSchema
from db.models import User as UserModel


def query_user_by_email(db: Session, email: str):
    user = db.query(UserModel).filter_by(email=email).first()
    return user


def query_user_by_id(db: Session, user_id: int):
    user = db.query(UserModel).filter_by(id=user_id).first()
    return user


def add_user(db: Session, user_data: UserRegisterSchema):
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
    return user
