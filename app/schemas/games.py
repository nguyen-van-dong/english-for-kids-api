from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime

# --- Quiz Question Schemas ---
class QuizQuestionBase(BaseModel):
    category_id: Optional[str] = "general"
    level: str = "easy"
    question_type: str = "picture-word"
    question: str
    target_word: str
    prompt_emoji: Optional[str] = "❓"
    prompt_audio: Optional[str] = None
    prompt_image_url: Optional[str] = None
    options: List[Any] # list of options
    explanation: Optional[str] = None
    reward_stars: int = 1
    order_index: int = 0
    is_active: bool = True

class QuizQuestionCreate(QuizQuestionBase):
    id: str

class QuizQuestionUpdate(BaseModel):
    category_id: Optional[str] = None
    level: Optional[str] = None
    question_type: Optional[str] = None
    question: Optional[str] = None
    target_word: Optional[str] = None
    prompt_emoji: Optional[str] = None
    prompt_audio: Optional[str] = None
    prompt_image_url: Optional[str] = None
    options: Optional[List[Any]] = None
    explanation: Optional[str] = None
    reward_stars: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class QuizQuestionResponse(QuizQuestionBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Spelling Word Schemas ---
class SpellingWordBase(BaseModel):
    word: str
    emoji: str = "✨"
    hint: str
    level: str = "easy"
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    reward_stars: int = 1
    order_index: int = 0
    is_active: bool = True

class SpellingWordCreate(SpellingWordBase):
    id: str

class SpellingWordUpdate(BaseModel):
    word: Optional[str] = None
    emoji: Optional[str] = None
    hint: Optional[str] = None
    level: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    reward_stars: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class SpellingWordResponse(SpellingWordBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Speaking Challenge Schemas ---
class SpeakingChallengeBase(BaseModel):
    text: str
    phonetic: Optional[str] = None
    emoji: str = "🗣️"
    level: str = "easy"
    fun_fact: Optional[str] = None
    pass_threshold_percent: int = 70
    reward_stars: int = 2
    order_index: int = 0
    is_active: bool = True

class SpeakingChallengeCreate(SpeakingChallengeBase):
    id: str

class SpeakingChallengeUpdate(BaseModel):
    text: Optional[str] = None
    phonetic: Optional[str] = None
    emoji: Optional[str] = None
    level: Optional[str] = None
    fun_fact: Optional[str] = None
    pass_threshold_percent: Optional[int] = None
    reward_stars: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class SpeakingChallengeResponse(SpeakingChallengeBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GamesSyncBundle(BaseModel):
    version: int
    quizzes: List[QuizQuestionResponse]
    spelling_words: List[SpellingWordResponse]
    speaking_challenges: List[SpeakingChallengeResponse]
    synced_at: str
