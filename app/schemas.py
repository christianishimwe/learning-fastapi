from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user_id: int


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
    email: str


class PostOut(BaseModel):
    post: Post
    owned_by: UserOut


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class VoteIn(BaseModel):
    post_id: int
    dir: int


class VoteOut(BaseModel):
    post_id: int
    user_id: int
