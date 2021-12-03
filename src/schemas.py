import re
from typing import Optional 
from datetime import datetime 
from pydantic import BaseModel,EmailStr,constr,validator

class UserBaseSchema(BaseModel):
    username: str 
    email: EmailStr 
    bio: Optional[constr(max_length=400)] = None 
    location: Optional[str] = None 
    website: Optional[str] = None 
    phone_number: Optional[str] = None
    class Config:
        orm_mode=True 

class UserRegisterSchema(UserBaseSchema):
    password: str 
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    @validator("password")
    def validate_password(cls,v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,50}$"
        if len(v) < 8:
            raise ValueError("Pasword must be longer than 8 characters.")
        password_valid = re.search(re.compile(pattern), v)
        if not password_valid:
            raise ValueError("Password must contain an uppercase letter, lowercase letter, digit, and special character.")
        return v.strip()

class UserLoginSchema(BaseModel):
    email: EmailStr 
    password: str 

class UserUpdateSchema(BaseModel):
    bio: Optional[constr(max_length=400)] = None 
    location: Optional[str] = None 
    website: Optional[str] = None 
    phone_number: Optional[str] = None
    updated_at: datetime = datetime.utcnow()

class BucketSchema(BaseModel):
    goal: str 
    category: str 
    active:bool= True 
    visibility: str="private"
    due_date: datetime = None
    created_at: datetime = datetime.utcnow()
    @validator("visibility")
    def validate_visibility(cls,v):
        if v not in ["public","private"]:
            raise ValueError("Visibility must be public or private.")
        return v

class BucketUpdateSchema(BaseModel):
    goal: str 
    category: str 
    active:bool= True 
    visibility: str="private"
    due_date: datetime = None
    updated_at: datetime = datetime.utcnow()
    @validator("visibility")
    def validate_visibility(cls,v):
        if v not in ["public","private"]:
            raise ValueError("Visibility must be public or private.")
        return v