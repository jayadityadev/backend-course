from pydantic import BaseModel, EmailStr
from datetime import datetime

# Post management schema

class PostBase(BaseModel):
    title: str
    content: str
    category: str = "Generic"
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True

# User management schema

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Login management schema

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None