from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_user_service
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, ProgressSync
from app.services.user_service import UserService

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """
    Get current logged in user and child profile.
    """
    return user_service.get_profile(current_user)

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """
    Update parent info, child name, age, or avatar.
    """
    return user_service.update_profile(current_user, user_in)

@router.post("/me/sync-progress", response_model=UserResponse)
def sync_user_progress(
    progress_in: ProgressSync,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """
    Sync stars, streak, mastered words, and high scores from mobile app.
    """
    return user_service.sync_progress(current_user, progress_in)
