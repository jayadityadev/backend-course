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

class PostResponse(PostBase):
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

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Login management schema

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str | None = None
