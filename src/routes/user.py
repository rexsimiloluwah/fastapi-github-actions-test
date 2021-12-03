from fastapi import HTTPException,APIRouter,Depends 
from schemas import UserUpdateSchema
from dependency import get_db 
from helpers.auth import JwtAuthHelper
from controllers import user as user_controller
from sqlalchemy.orm import Session
auth_helper = JwtAuthHelper()

router = APIRouter()

@router.get("/user",response_model=dict)
def get_user(db:Session=Depends(get_db),user_id:int=Depends(auth_helper.auth_wrapper)):
    return user_controller.get_user(db,user_id)

@router.put("/user",response_model=dict)
def update_user(user_data:UserUpdateSchema,db:Session=Depends(get_db),user_id:int=Depends(auth_helper.auth_wrapper)):
    return user_controller.update_user(db,user_data,user_id)

@router.delete("/user",response_model=dict)
def delete_user(db:Session=Depends(get_db),user_id:int=Depends(auth_helper.auth_wrapper)):
    return user_controller.delete_user(db,user_id)

@router.get("/user/buckets",response_model=dict)
def get_user_buckets(db:Session=Depends(get_db),user_id:int=Depends(auth_helper.auth_wrapper)):
    return user_controller.get_user_buckets(db,user_id)

@router.get("/user/bucket/{bucket_id}",response_model=dict)
def get_user_bucket_by_id(bucket_id:int,db:Session=Depends(get_db),user_id:int=Depends(auth_helper.auth_wrapper)):
    return user_controller.get_user_bucket_by_id(db,user_id,bucket_id)

@router.get("/user/{user_id}",response_model=dict)
def get_user_by_id(user_id:int,db:Session=Depends(get_db)):
    return user_controller.get_user_by_id(db,user_id)




