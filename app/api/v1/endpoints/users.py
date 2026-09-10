from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, ProgressSync
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current logged in user and child profile.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update parent info, child name, age, or avatar.
    """
    if user_in.parent_name is not None:
        current_user.parent_name = user_in.parent_name
    if user_in.child_name is not None:
        current_user.child_name = user_in.child_name
    if user_in.child_age is not None:
        current_user.child_age = user_in.child_age
    if user_in.avatar is not None:
        current_user.avatar = user_in.avatar

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/sync-progress", response_model=UserResponse)
def sync_user_progress(
    progress_in: ProgressSync,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sync stars, streak, mastered words, and high scores from mobile app.
    """
    if progress_in.stars is not None:
        current_user.stars = max(current_user.stars, progress_in.stars)
    if progress_in.streak_days is not None:
        current_user.streak_days = max(current_user.streak_days, progress_in.streak_days)
    if progress_in.last_active_date is not None:
        current_user.last_active_date = progress_in.last_active_date
    if progress_in.mastered_words is not None:
        # Merge mastered words list uniquely
        existing = set(current_user.mastered_words or [])
        updated = list(existing.union(set(progress_in.mastered_words)))
        current_user.mastered_words = updated
    if progress_in.completed_categories is not None:
        existing_cat = set(current_user.completed_categories or [])
        updated_cat = list(existing_cat.union(set(progress_in.completed_categories)))
        current_user.completed_categories = updated_cat
    if progress_in.quiz_high_score is not None:
        current_user.quiz_high_score = max(current_user.quiz_high_score, progress_in.quiz_high_score)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
