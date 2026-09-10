from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    parent_name = Column(String, default="")
    child_name = Column(String, default="Little Explorer", nullable=False)
    child_age = Column(Integer, default=5, nullable=False)
    avatar = Column(String, default="🦁", nullable=False)
    
    # Progress & Gamification fields
    stars = Column(Integer, default=10)
    streak_days = Column(Integer, default=1)
    last_active_date = Column(String, default="")
    mastered_words = Column(JSON, default=list)
    completed_categories = Column(JSON, default=list)
    quiz_high_score = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
