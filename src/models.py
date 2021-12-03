from database import Base 
from datetime import datetime
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from sqlalchemy import Boolean,Column,String,Integer,ForeignKey,DateTime,Enum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    bio = Column(String,nullable=True)
    location = Column(String,nullable=True)
    website = Column(String,nullable=True)
    phone_number = Column(String,nullable=True)
    created_at = Column(DateTime,nullable=False,default=datetime.utcnow)
    updated_at = Column(DateTime,nullable=False,default=datetime.utcnow)
    bucket_list = relationship("Bucket",back_populates="user")

    def set_password(self,password:str)->None:
        self.password = pwd_context.hash(password)

    def check_password(self,password:str)->bool:
        return pwd_context.verify(password,self.password)

    def __repr__(self)->str:
        return f"id: {self.id}, Email: {self.email}"

class Bucket(Base):
    __tablename__ = "buckets"
    id = Column(Integer,primary_key=True)
    goal = Column(String,nullable=False)
    category = Column(String,nullable=False)
    active = Column(Boolean,nullable=False,default=True)
    visibility = Column(String,Enum("public","private"),nullable=True,default="public")
    user_id = Column(Integer,ForeignKey("users.id"))
    due_date = Column(DateTime,nullable=True)
    created_at = Column(DateTime,nullable=False,default=datetime.utcnow)
    updated_at = Column(DateTime,nullable=False,default=datetime.utcnow)
    user = relationship("User",back_populates="bucket_list")

    def __repr__(self)->str:
        return f"id: {self.id}, Goal: {self.goal}"
