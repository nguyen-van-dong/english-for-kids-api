from datetime import datetime
from typing import List, Dict, Any

from app.models.user import User
from app.models.learning import StudySession, TimelineEvent, WordProgress
from app.repositories.user_repository import UserRepository
from app.repositories.learning_repository import (
    StudySessionRepository,
    TimelineEventRepository,
    WordProgressRepository,
)
from app.schemas.learning import SyncAllPayload, LearningReportResponse

class LearningService:
    def __init__(
        self,
        user_repo: UserRepository,
        session_repo: StudySessionRepository,
        timeline_repo: TimelineEventRepository,
        word_repo: WordProgressRepository,
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.timeline_repo = timeline_repo
        self.word_repo = word_repo

    def sync_all(self, user: User, payload: SyncAllPayload) -> Dict[str, Any]:
        """
        Synchronize all offline study sessions, timeline events, and word progress into the database.
        """
        # 1. Update total study minutes
        if payload.total_study_minutes is not None:
            self.user_repo.update_total_study_minutes(user, payload.total_study_minutes)

        # 2. Upsert study sessions
        if payload.study_sessions:
            for s_in in payload.study_sessions:
                self.session_repo.upsert_session(user.id, s_in)

        # 3. Upsert timeline events
        if payload.timeline_events:
            for ev_in in payload.timeline_events:
                self.timeline_repo.upsert_event(user.id, ev_in)

        # 4. Upsert word progress
        if payload.word_progress:
            for word_id, wp_in in payload.word_progress.items():
                self.word_repo.upsert_word_progress(user.id, word_id, wp_in)

        return {
            "success": True,
            "message": "All learning sessions, timeline events, and word progress synced successfully to database!",
            "user_id": user.id,
            "synced_at": datetime.utcnow().isoformat()
        }

    def get_timeline(self, user: User, limit: int = 30) -> List[TimelineEvent]:
        return self.timeline_repo.get_recent_by_user_id(user.id, limit=limit)

    def get_sessions(self, user: User, limit: int = 20) -> List[StudySession]:
        return self.session_repo.get_by_user_id(user.id, limit=limit)

    def get_word_progress(self, user: User) -> List[WordProgress]:
        return self.word_repo.get_all_by_user_id(user.id)

    def get_learning_report(self, user: User) -> LearningReportResponse:
        """
        Calculate consolidated metrics for Parent Dashboard.
        """
        today_str = datetime.utcnow().strftime("%Y-%m-%d")

        # 1. Calculate today's study minutes
        today_sessions = self.session_repo.get_sessions_by_date_prefix(user.id, today_str)
        today_seconds = sum(s.duration_seconds for s in today_sessions)
        today_minutes = max(1, round(today_seconds / 60))

        # 2. Calculate speech metrics
        speech_events = self.timeline_repo.get_by_type(user.id, "SPEECH_SCORED")
        speech_count = len(speech_events)
        avg_accuracy = (
            round(sum(e.score or 0 for e in speech_events) / speech_count)
            if speech_count > 0
            else 85
        )

        # 3. Calculate quiz count
        quiz_count = self.timeline_repo.count_by_type(user.id, "QUIZ_ANSWERED")

        # 4. Words mastered count
        mastered_count = self.word_repo.count_mastered(user.id)

        # 5. Recent timeline
        recent_events = self.timeline_repo.get_recent_by_user_id(user.id, limit=10)

        return LearningReportResponse(
            child_name=user.child_name,
            avatar=user.avatar,
            total_stars=user.stars,
            streak_days=user.streak_days,
            today_study_minutes=today_minutes,
            total_study_minutes=user.total_study_minutes or today_minutes,
            words_mastered_count=mastered_count,
            speech_practices_count=speech_count,
            average_speech_accuracy=avg_accuracy,
            total_quizzes_completed=quiz_count,
            recent_timeline=recent_events,
        )
