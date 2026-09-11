from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime

# --- Home Banner Schemas ---
class HomeBannerBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    image_url: str
    action_type: str = "NAVIGATE_CATEGORY"
    action_payload: str = "animals"
    background_color: str = "#4D96FF"
    display_order: int = 0
    is_active: bool = True

class HomeBannerCreate(HomeBannerBase):
    id: str

class HomeBannerUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    image_url: Optional[str] = None
    action_type: Optional[str] = None
    action_payload: Optional[str] = None
    background_color: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class HomeBannerResponse(HomeBannerBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Daily Quest Schemas ---
class DailyQuestBase(BaseModel):
    title: str
    description: Optional[str] = None
    emoji: str = "🎯"
    target_type: str = "WORDS_PRACTICED"
    target_count: int = 3
    reward_stars: int = 3
    day_of_week: Optional[int] = None
    order_index: int = 0
    is_active: bool = True

class DailyQuestCreate(DailyQuestBase):
    id: str

class DailyQuestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    target_type: Optional[str] = None
    target_count: Optional[int] = None
    reward_stars: Optional[int] = None
    day_of_week: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class DailyQuestResponse(DailyQuestBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Gamification Schemas ---
class AchievementBadgeBase(BaseModel):
    title: str
    description: str
    badge_icon: str = "🏆"
    badge_image_url: Optional[str] = None
    condition_type: str = "STREAK_DAYS"
    condition_value: int = 1
    reward_stars: int = 5
    order_index: int = 0
    is_active: bool = True

class AchievementBadgeCreate(AchievementBadgeBase):
    id: str

class AchievementBadgeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    badge_icon: Optional[str] = None
    badge_image_url: Optional[str] = None
    condition_type: Optional[str] = None
    condition_value: Optional[int] = None
    reward_stars: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class AchievementBadgeResponse(AchievementBadgeBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AvatarCharacterBase(BaseModel):
    name: str
    emoji: str = "🦁"
    image_url: Optional[str] = None
    unlock_type: str = "free"
    price_stars: int = 0
    required_level: int = 1
    order_index: int = 0
    is_active: bool = True

class AvatarCharacterCreate(AvatarCharacterBase):
    id: str

class AvatarCharacterUpdate(BaseModel):
    name: Optional[str] = None
    emoji: Optional[str] = None
    image_url: Optional[str] = None
    unlock_type: Optional[str] = None
    price_stars: Optional[int] = None
    required_level: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class AvatarCharacterResponse(AvatarCharacterBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StickerItemBase(BaseModel):
    name: str
    emoji: str = "🚀"
    image_url: Optional[str] = None
    category_name: str = "General"
    price_stars: int = 5
    order_index: int = 0
    is_active: bool = True

class StickerItemCreate(StickerItemBase):
    id: str

class StickerItemUpdate(BaseModel):
    name: Optional[str] = None
    emoji: Optional[str] = None
    image_url: Optional[str] = None
    category_name: Optional[str] = None
    price_stars: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class StickerItemResponse(StickerItemBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- App Setting Schemas ---
class AppSettingBase(BaseModel):
    config_key: str
    config_value: str
    data_type: str = "string"
    description: Optional[str] = None
    is_public: bool = True

class AppSettingCreate(AppSettingBase):
    pass

class AppSettingUpdate(BaseModel):
    config_value: Optional[str] = None
    data_type: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class AppSettingResponse(AppSettingBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
