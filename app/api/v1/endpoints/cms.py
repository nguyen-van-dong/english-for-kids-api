from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cms import HomeBanner, DailyQuest, AppSetting, ContentVersion
from app.models.gamification import AchievementBadge, AvatarCharacter, StickerItem
from app.schemas.cms import (
    HomeBannerResponse,
    DailyQuestResponse,
    AchievementBadgeResponse,
    AvatarCharacterResponse,
    StickerItemResponse,
    AppSettingResponse,
)

router = APIRouter()

@router.get("/banners", response_model=List[HomeBannerResponse])
def get_home_banners(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False)
):
    """
    Get active home carousels/banners.
    """
    query = db.query(HomeBanner)
    if not include_inactive:
        query = query.filter(HomeBanner.is_active == True)
    return query.order_by(HomeBanner.display_order.asc()).all()


@router.get("/daily-quests", response_model=List[DailyQuestResponse])
def get_daily_quests(
    db: Session = Depends(get_db),
    day_of_week: int = Query(None, description="0=Mon, 6=Sun"),
    include_inactive: bool = Query(False)
):
    """
    Get active daily quests.
    """
    query = db.query(DailyQuest)
    if not include_inactive:
        query = query.filter(DailyQuest.is_active == True)
    if day_of_week is not None:
        query = query.filter((DailyQuest.day_of_week == day_of_week) | (DailyQuest.day_of_week == None))

    return query.order_by(DailyQuest.order_index.asc()).all()


@router.get("/badges", response_model=List[AchievementBadgeResponse])
def get_achievement_badges(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False)
):
    """
    Get all achievement badges.
    """
    query = db.query(AchievementBadge)
    if not include_inactive:
        query = query.filter(AchievementBadge.is_active == True)
    return query.order_by(AchievementBadge.order_index.asc()).all()


@router.get("/avatars", response_model=List[AvatarCharacterResponse])
def get_avatars(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False)
):
    """
    Get all available avatar characters for kids.
    """
    query = db.query(AvatarCharacter)
    if not include_inactive:
        query = query.filter(AvatarCharacter.is_active == True)
    return query.order_by(AvatarCharacter.order_index.asc()).all()


@router.get("/stickers", response_model=List[StickerItemResponse])
def get_stickers(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False)
):
    """
    Get all stickers in the virtual store.
    """
    query = db.query(StickerItem)
    if not include_inactive:
        query = query.filter(StickerItem.is_active == True)
    return query.order_by(StickerItem.order_index.asc()).all()


@router.get("/settings", response_model=Dict[str, Any])
def get_public_settings(db: Session = Depends(get_db)):
    """
    Get all public application remote configurations as a simple key-value dictionary.
    """
    settings_rows = db.query(AppSetting).filter(AppSetting.is_public == True).all()
    config_dict = {}
    for row in settings_rows:
        val = row.config_value
        if row.data_type == "number":
            val = float(val) if "." in val else int(val)
        elif row.data_type == "boolean":
            val = val.lower() in ["true", "1", "yes"]
        config_dict[row.config_key] = val
    return config_dict


@router.get("/versions", response_model=Dict[str, int])
def get_content_versions(db: Session = Depends(get_db)):
    """
    Check current version of each content module to detect if mobile app needs to re-sync.
    """
    versions = db.query(ContentVersion).all()
    return {v.id: v.version_number for v in versions}
