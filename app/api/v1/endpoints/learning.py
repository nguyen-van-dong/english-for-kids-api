from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.learning import StudySession, TimelineEvent, WordProgress
from app.schemas.learning import (
    SyncAllPayload,
    StudySessionResponse,
    TimelineEventResponse,
    WordProgressResponse,
    LearningReportResponse,
)
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/sync-all")
def sync_all_learning_data(
    payload: SyncAllPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Synchronize all offline study sessions, timeline events, and word progress into the database.
    """
    # 1. Update user total study minutes
    if payload.total_study_minutes is not None:
        current_user.total_study_minutes = max(
            current_user.total_study_minutes or 0, payload.total_study_minutes
        )

    # 2. Upsert study sessions
    if payload.study_sessions:
        for s_in in payload.study_sessions:
            existing_session = db.query(StudySession).filter(
                StudySession.id == s_in.id,
                StudySession.user_id == current_user.id
            ).first()

            if not existing_session:
                new_session = StudySession(
                    id=s_in.id,
                    user_id=current_user.id,
                    started_at=s_in.started_at,
                    ended_at=s_in.ended_at,
                    duration_seconds=s_in.duration_seconds,
                    activities_count=s_in.activities_count,
                )
                db.add(new_session)
            else:
                existing_session.ended_at = s_in.ended_at
                existing_session.duration_seconds = max(existing_session.duration_seconds, s_in.duration_seconds)
                existing_session.activities_count = max(existing_session.activities_count, s_in.activities_count)

    # 3. Upsert timeline events
    if payload.timeline_events:
        for ev_in in payload.timeline_events:
            existing_event = db.query(TimelineEvent).filter(
                TimelineEvent.id == ev_in.id,
                TimelineEvent.user_id == current_user.id
            ).first()

            if not existing_event:
                new_event = TimelineEvent(
                    id=ev_in.id,
                    user_id=current_user.id,
                    event_type=ev_in.event_type,
                    title=ev_in.title,
                    target_word=ev_in.target_word,
                    category_title=ev_in.category_title,
                    score=ev_in.score,
                    stars_earned=ev_in.stars_earned or 0,
                    is_correct=ev_in.is_correct if ev_in.is_correct is not None else True,
                    timestamp=ev_in.timestamp,
                )
                db.add(new_event)

    # 4. Upsert word progress
    if payload.word_progress:
        for word_id, wp_in in payload.word_progress.items():
            existing_wp = db.query(WordProgress).filter(
                WordProgress.user_id == current_user.id,
                WordProgress.word_id == word_id
            ).first()

            if not existing_wp:
                new_wp = WordProgress(
                    user_id=current_user.id,
                    word_id=wp_in.word_id,
                    word=wp_in.word,
                    category_id=wp_in.category_id or "general",
                    status=wp_in.status or "learning",
                    accuracy_score=wp_in.accuracy_score or 0,
                    attempts_count=wp_in.attempts_count or 1,
                    last_practiced_at=wp_in.last_practiced_at,
                )
                db.add(new_wp)
            else:
                existing_wp.accuracy_score = max(existing_wp.accuracy_score, wp_in.accuracy_score or 0)
                existing_wp.attempts_count += 1
                if wp_in.status == "mastered" or (wp_in.accuracy_score or 0) >= 80:
                    existing_wp.status = "mastered"
                existing_wp.last_practiced_at = wp_in.last_practiced_at

    db.add(current_user)
    db.commit()

    return {
        "success": True,
        "message": "All learning sessions, timeline events, and word progress synced successfully to database!",
        "user_id": current_user.id,
        "synced_at": datetime.utcnow().isoformat()
    }


@router.get("/timeline", response_model=List[TimelineEventResponse])
def get_timeline_events(
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current child's activity timeline.
    """
    events = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.user_id == current_user.id)
        .order_by(TimelineEvent.created_at.desc())
        .limit(limit)
        .all()
    )
    return events


@router.get("/sessions", response_model=List[StudySessionResponse])
def get_study_sessions(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get recent study sessions.
    """
    sessions = (
        db.query(StudySession)
        .filter(StudySession.user_id == current_user.id)
        .order_by(StudySession.created_at.desc())
        .limit(limit)
        .all()
    )
    return sessions


@router.get("/word-progress", response_model=List[WordProgressResponse])
def get_word_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all word progress entries for the current child.
    """
    words = (
        db.query(WordProgress)
        .filter(WordProgress.user_id == current_user.id)
        .order_by(WordProgress.updated_at.desc())
        .all()
    )
    return words


@router.get("/report", response_model=LearningReportResponse)
def get_learning_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate consolidated report for Parent Dashboard.
    """
    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    # 1. Calculate today's study minutes
    today_sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id == current_user.id,
            StudySession.started_at.startswith(today_str)
        )
        .all()
    )
    today_seconds = sum(s.duration_seconds for s in today_sessions)
    today_minutes = max(1, round(today_seconds / 60))

    # 2. Calculate speech metrics
    speech_events = (
        db.query(TimelineEvent)
        .filter(
            TimelineEvent.user_id == current_user.id,
            TimelineEvent.event_type == "SPEECH_SCORED"
        )
        .all()
    )
    speech_count = len(speech_events)
    avg_accuracy = (
        round(sum(e.score or 0 for e in speech_events) / speech_count)
        if speech_count > 0
        else 85
    )

    # 3. Calculate quiz count
    quiz_count = (
        db.query(TimelineEvent)
        .filter(
            TimelineEvent.user_id == current_user.id,
            TimelineEvent.event_type == "QUIZ_ANSWERED"
        )
        .count()
    )

    # 4. Words mastered count
    mastered_count = (
        db.query(WordProgress)
        .filter(
            WordProgress.user_id == current_user.id,
            WordProgress.status == "mastered"
        )
        .count()
    )

    # 5. Recent timeline
    recent_events = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.user_id == current_user.id)
        .order_by(TimelineEvent.created_at.desc())
        .limit(10)
        .all()
    )

    return LearningReportResponse(
        child_name=current_user.child_name,
        avatar=current_user.avatar,
        total_stars=current_user.stars,
        streak_days=current_user.streak_days,
        today_study_minutes=today_minutes,
        total_study_minutes=current_user.total_study_minutes or today_minutes,
        words_mastered_count=mastered_count,
        speech_practices_count=speech_count,
        average_speech_accuracy=avg_accuracy,
        total_quizzes_completed=quiz_count,
        recent_timeline=recent_events,
    )
