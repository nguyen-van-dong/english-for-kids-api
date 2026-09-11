from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, index=True) # e.g. 'q_e1'
    category_id = Column(String, default="general", index=True)
    level = Column(String, default="easy", index=True) # 'easy', 'medium', 'hard'
    question_type = Column(String, default="picture-word", index=True) # 'picture-word', 'listening', 'spelling', etc.
    question = Column(String, nullable=False)
    target_word = Column(String, nullable=False)
    prompt_emoji = Column(String, default="❓")
    prompt_audio = Column(String, nullable=True)
    prompt_image_url = Column(String, nullable=True)
    options = Column(JSON, nullable=False) # list of {id, text, emoji, isCorrect, image_url}
    explanation = Column(Text, nullable=True)
    reward_stars = Column(Integer, default=1)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SpellingWord(Base):
    __tablename__ = "spelling_words"

    id = Column(String, primary_key=True, index=True) # e.g. 'sp_e1'
    word = Column(String, nullable=False, index=True)
    emoji = Column(String, default="✨", nullable=False)
    hint = Column(String, nullable=False)
    level = Column(String, default="easy", index=True) # 'easy', 'medium', 'hard'
    image_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    reward_stars = Column(Integer, default=1)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SpeakingChallenge(Base):
    __tablename__ = "speaking_challenges"

    id = Column(String, primary_key=True, index=True) # e.g. 'spk_e1'
    text = Column(String, nullable=False, index=True)
    phonetic = Column(String, nullable=True)
    emoji = Column(String, default="🗣️", nullable=False)
    level = Column(String, default="easy", index=True) # 'easy', 'medium', 'hard'
    fun_fact = Column(Text, nullable=True)
    pass_threshold_percent = Column(Integer, default=70) # e.g. 70% accuracy
    reward_stars = Column(Integer, default=2)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
