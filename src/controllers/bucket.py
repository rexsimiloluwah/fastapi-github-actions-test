from typing import List
from schemas import BucketSchema, BucketUpdateSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import User as UserModel, Bucket as BucketModel
from db.repository.bucket import (
    query_bucket_by_id,
    query_bucket_by_user_id,
    query_buckets_by_user_id,
    add_single_bucket,
    add_multiple_buckets,
    query_buckets_by_visibility,
)


def create_new_bucket(db: Session, bucket_data: BucketSchema, user_id: int):
    """
    @Route: POST /api/v1/bucket
    @Description: Create a new bucket in the database
    @Args:
        db {Session} - Database session
        bucket_data {BucketSchema} - Bucket data
        user_id {int} - User ID
    @Requires Auth: True
    """
    try:
        new_bucket = add_single_bucket(db, bucket_data, user_id)
        if new_bucket:
            return {
                "status": True,
                "message": "New bucket successfully added to bucket list.",
                "data": new_bucket,
            }
        else:
            raise HTTPException(status_code=422, detail="Bucket creation failed.")
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


def create_new_buckets(db: Session, buckets_data: List[BucketSchema], user_id: int):
    """
    @Route: POST /api/v1/buckets
    @Description: Create new buckets (multiple)
    @Args:
        db {Session} - Database Session
        buckets_data {[BucketSchema]} - List of buckets to be added
        user_id {int} - User ID
    """
    try:
        new_buckets = add_multiple_buckets(db, buckets_data, user_id)
        print(new_buckets)
        if new_buckets:
            return {
                "status": True,
                "message": f"{len(buckets_data)} buckets successfully added to bucket list.",
                "data": buckets_data,
            }
        else:
            raise HTTPException(status_code=422, detail="Buckets creation failed.")
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


def update_bucket(
    db: Session, bucket_data: BucketUpdateSchema, user_id: int, bucket_id: int
):
    """
    @Route: PUT /api/v1/bucket/{bucket_id}
    @Description: Update an existing bucket
    @Args:
        db {Session} - Database session
        bucket_data {BucketSchema} - Bucket data to be updated
        bucket_id {int} - ID of bucket to be updated in the database
        user_id {int} - User ID
    @Requires Auth: True
    """
    existing_bucket = db.query(BucketModel).filter_by(id=bucket_id)
    if not existing_bucket.first():
        raise HTTPException(detail="Bucket not found.", status_code=404)
    existing_bucket.update(bucket_data.dict())
    db.commit()
    updated_bucket = query_bucket_by_id(db, bucket_id)
    return {
        "status": True,
        "message": "New bucket successfully added to bucket list.",
        "data": updated_bucket,
    }


def delete_bucket(db: Session, user_id: int, bucket_id: int):
    """
    @Route: DELETE /api/v1/bucket/{bucket_id}
    @Description: Delete an existing bucket
    @Args:
        db {Session} - Database session
        bucket_id {int} - ID of bucket to be deleted from the database
        user_id {int} - User ID
    """
    existing_bucket = query_bucket_by_id(db, bucket_id)
    if not existing_bucket:
        raise HTTPException(detail="Bucket not found.", status_code=404)
    db.delete(existing_bucket)
    db.commit()
    return {
        "status": True,
        "message": "Bucket deleted successfully",
        "data": existing_bucket,
    }


def get_all_public_buckets(db: Session):
    """
    @Route: GET /api/v1/buckets/public
    @Description: Get all public buckets
    @Args:
        db {Session} - Database session
    @Requires Auth: True
    """
    public_buckets = query_buckets_by_visibility(db, visibility="public")
    if not public_buckets:
        raise HTTPException(detail="No public buckets found.", status_code=404)
    return {
        "status": True,
        "message": f"Successfully fetched {len(public_buckets)} buckets.",
        "data": public_buckets,
    }
