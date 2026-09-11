from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from app.models.learning import StudySession, TimelineEvent, WordProgress
from app.repositories.base import BaseRepository
from app.schemas.learning import StudySessionInput, TimelineEventInput, WordProgressInput

class StudySessionRepository(BaseRepository[StudySession]):
    def __init__(self, db: Session):
        super().__init__(StudySession, db)

    def get_by_user_id(self, user_id: int, limit: int = 20) -> List[StudySession]:
        return (
            self.db.query(StudySession)
            .filter(StudySession.user_id == user_id)
            .order_by(StudySession.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_sessions_by_date_prefix(self, user_id: int, date_prefix: str) -> List[StudySession]:
        return (
            self.db.query(StudySession)
            .filter(
                StudySession.user_id == user_id,
                StudySession.started_at.startswith(date_prefix)
            )
            .all()
        )

    def upsert_session(self, user_id: int, s_in: StudySessionInput) -> StudySession:
        existing = (
            self.db.query(StudySession)
            .filter(
                StudySession.id == s_in.id,
                StudySession.user_id == user_id
            )
            .first()
        )
        if not existing:
            new_session = StudySession(
                id=s_in.id,
                user_id=user_id,
                started_at=s_in.started_at,
                ended_at=s_in.ended_at,
                duration_seconds=s_in.duration_seconds,
                activities_count=s_in.activities_count,
            )
            return self.create(new_session)
        else:
            existing.ended_at = s_in.ended_at
            existing.duration_seconds = max(existing.duration_seconds, s_in.duration_seconds)
            existing.activities_count = max(existing.activities_count, s_in.activities_count)
            return self.save(existing)


class TimelineEventRepository(BaseRepository[TimelineEvent]):
    def __init__(self, db: Session):
        super().__init__(TimelineEvent, db)

    def get_recent_by_user_id(self, user_id: int, limit: int = 30) -> List[TimelineEvent]:
        return (
            self.db.query(TimelineEvent)
            .filter(TimelineEvent.user_id == user_id)
            .order_by(TimelineEvent.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_type(self, user_id: int, event_type: str) -> List[TimelineEvent]:
        return (
            self.db.query(TimelineEvent)
            .filter(
                TimelineEvent.user_id == user_id,
                TimelineEvent.event_type == event_type
            )
            .all()
        )

    def count_by_type(self, user_id: int, event_type: str) -> int:
        return (
            self.db.query(TimelineEvent)
            .filter(
                TimelineEvent.user_id == user_id,
                TimelineEvent.event_type == event_type
            )
            .count()
        )

    def upsert_event(self, user_id: int, ev_in: TimelineEventInput) -> TimelineEvent:
        existing = (
            self.db.query(TimelineEvent)
            .filter(
                TimelineEvent.id == ev_in.id,
                TimelineEvent.user_id == user_id
            )
            .first()
        )
        if not existing:
            new_event = TimelineEvent(
                id=ev_in.id,
                user_id=user_id,
                event_type=ev_in.event_type,
                title=ev_in.title,
                target_word=ev_in.target_word,
                category_title=ev_in.category_title,
                score=ev_in.score,
                stars_earned=ev_in.stars_earned or 0,
                is_correct=ev_in.is_correct if ev_in.is_correct is not None else True,
                timestamp=ev_in.timestamp,
            )
            return self.create(new_event)
        return existing


class WordProgressRepository(BaseRepository[WordProgress]):
    def __init__(self, db: Session):
        super().__init__(WordProgress, db)

    def get_all_by_user_id(self, user_id: int) -> List[WordProgress]:
        return (
            self.db.query(WordProgress)
            .filter(WordProgress.user_id == user_id)
            .order_by(WordProgress.updated_at.desc())
            .all()
        )

    def count_mastered(self, user_id: int) -> int:
        return (
            self.db.query(WordProgress)
            .filter(
                WordProgress.user_id == user_id,
                WordProgress.status == "mastered"
            )
            .count()
        )

    def upsert_word_progress(
        self,
        user_id: int,
        word_id: str,
        wp_in: WordProgressInput
    ) -> WordProgress:
        existing = (
            self.db.query(WordProgress)
            .filter(
                WordProgress.user_id == user_id,
                WordProgress.word_id == word_id
            )
            .first()
        )
        if not existing:
            new_wp = WordProgress(
                user_id=user_id,
                word_id=wp_in.word_id,
                word=wp_in.word,
                category_id=wp_in.category_id or "general",
                status=wp_in.status or "learning",
                accuracy_score=wp_in.accuracy_score or 0,
                attempts_count=wp_in.attempts_count or 1,
                last_practiced_at=wp_in.last_practiced_at,
            )
            return self.create(new_wp)
        else:
            existing.accuracy_score = max(existing.accuracy_score, wp_in.accuracy_score or 0)
            existing.attempts_count += 1
            if wp_in.status == "mastered" or (wp_in.accuracy_score or 0) >= 80:
                existing.status = "mastered"
            existing.last_practiced_at = wp_in.last_practiced_at
            return self.save(existing)
