from fastapi import HTTPException, Depends, APIRouter
from schemas import BucketUpdateSchema, BucketSchema
from sqlalchemy.orm import Session
from controllers import bucket as bucket_controller
from dependency import get_db
from helpers.auth import JwtAuthHelper
from typing import List

router = APIRouter()
auth_helper = JwtAuthHelper()

@router.post("/bucket", response_model=dict)
def create_bucket(
    bucket_data: BucketSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(auth_helper.auth_wrapper),
):
    return bucket_controller.create_new_bucket(db, bucket_data, user_id)


@router.post("/buckets", response_model=dict)
def create_buckets(
    buckets_data: List[BucketSchema],
    db: Session = Depends(get_db),
    user_id: int = Depends(auth_helper.auth_wrapper),
):
    return bucket_controller.create_new_buckets(db, buckets_data, user_id)


@router.put("/bucket/{bucket_id}", response_model=dict)
def update_bucket(
    bucket_id: int,
    bucket_data: BucketUpdateSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(auth_helper.auth_wrapper),
):
    return bucket_controller.update_bucket(db, bucket_data, user_id, bucket_id)


@router.delete("/bucket/{bucket_id}", response_model=dict)
def delete_bucket(
    bucket_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(auth_helper.auth_wrapper),
):
    return bucket_controller.delete_bucket(db, user_id, bucket_id)


@router.get("/buckets/public", response_model=dict)
def get_public_buckets(db: Session = Depends(get_db)):
    return bucket_controller.get_all_public_buckets(db)
