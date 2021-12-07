from typing import Any
from sqlalchemy.orm import Session
from schemas import BucketSchema
from db.models import Bucket as BucketModel


def query_bucket_by_id(db: Session, bucket_id: int):
    bucket = db.query(BucketModel).filter_by(id=bucket_id).first()
    return bucket


def query_bucket_by_user_id(db: Session, user_id: int, bucket_id: int):
    bucket = db.query(BucketModel).filter_by(id=bucket_id, user_id=user_id).first()
    return bucket


def query_buckets_by_user_id(db: Session, user_id: int):
    buckets = db.query(BucketModel).filter_by(user_id=user_id).all()
    return buckets


def query_buckets_by_visibility(db: Session, visibility: str = "public"):
    buckets = db.query(BucketModel).filter_by(visibility=visibility).all()
    return buckets


def query_user_buckets_by_visibility(
    db: Session, user_id: int, visibility: str = "public"
):
    buckets = (
        db.query(BucketModel).filter_by(user_id=user_id, visibility=visibility).all()
    )
    return buckets


def add_single_bucket(db: Session, bucket_data: BucketSchema, user_id: int):
    new_bucket = BucketModel(**bucket_data.dict(), user_id=user_id)
    db.add(new_bucket)
    db.commit()
    db.refresh(new_bucket)
    return new_bucket


def add_multiple_buckets(db: Session, buckets_data: [BucketSchema], user_id: int):
    new_buckets = [
        BucketModel(**bucket_data.dict(), user_id=user_id)
        for bucket_data in buckets_data
    ]
    db.bulk_save_objects(new_buckets)
    db.commit()
    return new_buckets
