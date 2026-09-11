from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class StudySessionBase(BaseModel):
    id: str
    started_at: str
    ended_at: Optional[str] = None
    duration_seconds: int = 0
    activities_count: int = 0

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionResponse(StudySessionBase):
    user_id: int

    class Config:
        from_attributes = True


class TimelineEventBase(BaseModel):
    id: str
    event_type: str
    title: str
    target_word: Optional[str] = None
    category_title: Optional[str] = None
    score: Optional[int] = None
    stars_earned: Optional[int] = 0
    is_correct: Optional[bool] = True
    timestamp: str

class TimelineEventCreate(TimelineEventBase):
    pass

class TimelineEventResponse(TimelineEventBase):
    user_id: int

    class Config:
        from_attributes = True


class WordProgressBase(BaseModel):
    word_id: str
    word: str
    category_id: Optional[str] = "general"
    status: Optional[str] = "learning"
    accuracy_score: Optional[int] = 0
    attempts_count: Optional[int] = 1
    last_practiced_at: str

class WordProgressCreate(WordProgressBase):
    pass

class WordProgressResponse(WordProgressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class SyncAllPayload(BaseModel):
    total_study_minutes: Optional[int] = None
    study_sessions: Optional[List[StudySessionCreate]] = []
    timeline_events: Optional[List[TimelineEventCreate]] = []
    word_progress: Optional[Dict[str, WordProgressCreate]] = {}


class LearningReportResponse(BaseModel):
    child_name: str
    avatar: str
    total_stars: int
    streak_days: int
    today_study_minutes: int
    total_study_minutes: int
    words_mastered_count: int
    speech_practices_count: int
    average_speech_accuracy: int
    total_quizzes_completed: int
    recent_timeline: List[TimelineEventResponse]
