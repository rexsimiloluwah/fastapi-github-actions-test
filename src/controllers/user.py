from schemas import (
    UserUpdateSchema,
    BucketSchema
)
from models import (
    User as UserModel,
    Bucket as BucketModel
)
from sqlalchemy.orm import Session 
from fastapi import HTTPException 

def get_user(db:Session,user_id:int):
    """
        @Route: GET /api/v1/user
        @Description: Get a full user profile 
        @Args: 
            db {Session} - Database session 
            user_id {int} - User ID
        @Requires Auth: True
    """
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(detail="User does not exist.",status_code=404)
    user_buckets = db.query(BucketModel).filter_by(user_id=user_id).all()
    return {
        "status":True,
        "message":"Successfully fetched user.",
        "data":{
            "user":user,
            "buckets":user_buckets
        }
    }

def update_user(db:Session,user_data:UserUpdateSchema,user_id:int):
    """
        @Route: PUT /api/v1/user
        @Description: Update a user's profile
        @Args: 
            db {Session} - Database session 
            user_data {UserSchema} - User Schema
            user_id {int} - User ID
        @Requires Auth: True
    """
    existing_user = db.query(UserModel).filter_by(id=user_id)
    if not existing_user.first():
        raise HTTPException(detail="User does not exist.",status_code=404)
    existing_user.update(user_data.dict())
    db.commit()
    updated_user = db.query(UserModel).filter_by(id=user_id).first()
    return {
        "status":True,
        "message":"Successfully updated user.",
        "data": updated_user
    }

def delete_user(db:Session,user_id:int):
    """
        @Route: DELETE /api/v1/user
        @Description: Get a full user profile 
        @Args: 
            db {Session} - Database session 
            user_id {int} - User ID
        @Requires Auth: True
    """
    existing_user = db.query(UserModel).filter_by(id=user_id).first()
    if not existing_user:
        raise HTTPException(detail="User does not exist.",status_code=404)
    db.delete(existing_user)
    db.commit()
    return {
        "status":True,
        "message":"Successfully deleted user.",
        "data": existing_user
    }

def get_user_by_id(db:Session,user_id:int):
    """
        @Route: GET /api/v1/user/{user_id}
        @Description: Get user by ID (public)
        @Args:
            db {Session} - Database Session 
            user_id {int} - User ID
        @Requires Auth: False
    """
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User does not exist.")
    user_public_buckets = db.query(BucketModel).filter_by(user_id=user_id,visibility="public").all()
    return {
        "status":True,
        "message":"Successfully fetched user.",
        "data": {
            "user":user,
            "buckets":user_public_buckets
        }
    }

def get_user_buckets(db:Session,user_id:int):
    """
        @Route: GET /api/v1/user/buckets
        @Description: Get user buckets
        @Args:
            db {Session} - Database Session 
            user_id {int} - User ID 
        @Requires Auth: True
    """
    user_buckets = db.query(BucketModel).filter_by(user_id=user_id).all()
    if not user_buckets:
        raise HTTPException(detail="No buckets for this user.",status_code=404)
    return {
        "status":True,
        "message":"Successfully fetched user's buckets.",
        "data":user_buckets
    }

def get_user_bucket_by_id(db:Session,user_id:int,bucket_id:int):
    """
        @Route: GET /api/v1/user/bucket/{bucket_id}
        @Description: Get user buckets by ID 
        @Args: 
            db {Session} - Database Session 
            user_id {int} - User ID 
            bucket_id {int} - Bucket ID 
        @Requires Auth: True 
    """
    user_bucket = db.query(BucketModel).filter_by(id=bucket_id,user_id=user_id).first()
    print(user_bucket)
    if not user_bucket:
        raise HTTPException(detail="User bucket does not exist.", status_code=404)
    return {
        "status":True,
        "message":"Successfully fetched user bucket.",
        "data":user_bucket
    }



    