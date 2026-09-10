from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Base properties
class UserBase(BaseModel):
    email: EmailStr
    parent_name: Optional[str] = ""
    child_name: str = "Little Explorer"
    child_age: int = 5
    avatar: str = "🦁"

# Properties to receive via API on creation
class UserRegister(UserBase):
    password: str

# Properties to receive via API on login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str
    user: "UserResponse"

# Properties to update profile
class UserUpdate(BaseModel):
    parent_name: Optional[str] = None
    child_name: Optional[str] = None
    child_age: Optional[int] = None
    avatar: Optional[str] = None

# Properties to sync progress
class ProgressSync(BaseModel):
    stars: Optional[int] = None
    streak_days: Optional[int] = None
    last_active_date: Optional[str] = None
    mastered_words: Optional[List[str]] = None
    completed_categories: Optional[List[str]] = None
    quiz_high_score: Optional[int] = None

# Properties to return to client
class UserResponse(UserBase):
    id: int
    stars: int
    streak_days: int
    last_active_date: Optional[str] = ""
    mastered_words: List[str] = []
    completed_categories: List[str] = []
    quiz_high_score: int = 0

    class Config:
        from_attributes = True

Token.model_rebuild()
