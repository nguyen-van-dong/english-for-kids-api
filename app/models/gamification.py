from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class AchievementBadge(Base):
    __tablename__ = "achievements_badges"

    id = Column(String, primary_key=True, index=True) # e.g. 'streak_7', 'vocab_50'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    badge_icon = Column(String, default="🏆", nullable=False)
    badge_image_url = Column(String, nullable=True)
    condition_type = Column(String, nullable=False, index=True) # 'STREAK_DAYS', 'WORDS_LEARNED', 'QUIZ_SCORE', 'SPEAKING_PASSED'
    condition_value = Column(Integer, default=1)
    reward_stars = Column(Integer, default=5)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AvatarCharacter(Base):
    __tablename__ = "avatars_characters"

    id = Column(String, primary_key=True, index=True) # e.g. 'avatar_lion', 'avatar_dragon'
    name = Column(String, nullable=False)
    emoji = Column(String, default="🦁", nullable=False)
    image_url = Column(String, nullable=True)
    unlock_type = Column(String, default="free", index=True) # 'free', 'level', 'stars'
    price_stars = Column(Integer, default=0)
    required_level = Column(Integer, default=1)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StickerItem(Base):
    __tablename__ = "stickers_store"

    id = Column(String, primary_key=True, index=True) # e.g. 'stk_rocket'
    name = Column(String, nullable=False)
    emoji = Column(String, default="🚀", nullable=False)
    image_url = Column(String, nullable=True)
    category_name = Column(String, default="General")
    price_stars = Column(Integer, default=5)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
