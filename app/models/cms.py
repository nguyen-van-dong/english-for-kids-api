from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class HomeBanner(Base):
    __tablename__ = "home_banners"

    id = Column(String, primary_key=True, index=True) # e.g. 'banner_summer_2026'
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    image_url = Column(String, nullable=False)
    action_type = Column(String, default="NAVIGATE_CATEGORY", index=True) # 'NAVIGATE_CATEGORY', 'NAVIGATE_GAME', 'EXTERNAL_URL'
    action_payload = Column(String, default="animals") # e.g. 'animals' or 'quiz'
    background_color = Column(String, default="#4D96FF")
    display_order = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DailyQuest(Base):
    __tablename__ = "daily_quests"

    id = Column(String, primary_key=True, index=True) # e.g. 'quest_learn_2_words'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    emoji = Column(String, default="🎯")
    target_type = Column(String, nullable=False, index=True) # 'WORDS_PRACTICED', 'QUIZ_PLAYED', 'SPEECH_RECORDED'
    target_count = Column(Integer, default=3)
    reward_stars = Column(Integer, default=3)
    day_of_week = Column(Integer, nullable=True) # 0=Monday, 6=Sunday, None=Everyday
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AppSetting(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String, unique=True, index=True, nullable=False)
    config_value = Column(Text, nullable=False)
    data_type = Column(String, default="string") # 'string', 'number', 'boolean', 'json'
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True) # whether visible to mobile client
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ContentVersion(Base):
    __tablename__ = "content_versions"

    id = Column(String, primary_key=True, index=True) # e.g. 'curriculum', 'games', 'gamification', 'cms'
    version_number = Column(Integer, default=1)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
