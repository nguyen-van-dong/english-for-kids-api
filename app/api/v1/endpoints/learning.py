from fastapi import APIRouter, Depends, Query
from typing import List

from app.api.deps import get_current_user, get_learning_service
from app.models.user import User
from app.schemas.learning import (
    SyncAllPayload,
    StudySessionResponse,
    TimelineEventResponse,
    WordProgressResponse,
    LearningReportResponse,
)
from app.services.learning_service import LearningService

router = APIRouter()

@router.post("/sync-all")
def sync_all_learning_data(
    payload: SyncAllPayload,
    current_user: User = Depends(get_current_user),
    learning_service: LearningService = Depends(get_learning_service),
):
    """
    Synchronize all offline study sessions, timeline events, and word progress into the database.
    """
    return learning_service.sync_all(current_user, payload)

@router.get("/timeline", response_model=List[TimelineEventResponse])
def get_timeline_events(
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    learning_service: LearningService = Depends(get_learning_service),
):
    """
    Get current child's activity timeline.
    """
    return learning_service.get_timeline(current_user, limit=limit)

@router.get("/sessions", response_model=List[StudySessionResponse])
def get_study_sessions(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    learning_service: LearningService = Depends(get_learning_service),
):
    """
    Get recent study sessions.
    """
    return learning_service.get_sessions(current_user, limit=limit)

@router.get("/word-progress", response_model=List[WordProgressResponse])
def get_word_progress(
    current_user: User = Depends(get_current_user),
    learning_service: LearningService = Depends(get_learning_service),
):
    """
    Get all word progress entries for the current child.
    """
    return learning_service.get_word_progress(current_user)

@router.get("/report", response_model=LearningReportResponse)
def get_learning_report(
    current_user: User = Depends(get_current_user),
    learning_service: LearningService = Depends(get_learning_service),
):
    """
    Calculate consolidated report for Parent Dashboard.
    """
    return learning_service.get_learning_report(current_user)
