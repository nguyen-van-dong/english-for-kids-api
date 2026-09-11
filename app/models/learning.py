from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(String, primary_key=True, index=True) # e.g. ses_1789234234
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(String, nullable=False)
    ended_at = Column(String, nullable=True)
    duration_seconds = Column(Integer, default=0, nullable=False)
    activities_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="study_sessions")


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(String, primary_key=True, index=True) # e.g. evt_1789234234_xyz
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True) # SPEECH_SCORED, QUIZ_ANSWERED, SPELLING_COMPLETED, WORD_MASTERED
    title = Column(String, nullable=False)
    target_word = Column(String, nullable=True)
    category_title = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    stars_earned = Column(Integer, default=0)
    is_correct = Column(Boolean, default=True)
    timestamp = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="timeline_events")


class WordProgress(Base):
    __tablename__ = "word_progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(String, nullable=False, index=True) # anim_1, spk_e1
    word = Column(String, nullable=False)
    category_id = Column(String, default="general")
    status = Column(String, default="learning") # learning, mastered
    accuracy_score = Column(Integer, default=0) # 0 to 100
    attempts_count = Column(Integer, default=1)
    last_practiced_at = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="word_progress_records")
