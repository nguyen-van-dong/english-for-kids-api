from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# --- Category Schemas ---
class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    icon: str = "paw"
    color: str = "#FF9671"
    light_color: str = "#FFF0EB"
    age_min: int = 3
    age_max: int = 10
    order_index: int = 0
    is_active: bool = True
    is_free: bool = True

class CategoryCreate(CategoryBase):
    id: str

class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    light_color: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None
    is_free: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: str
    word_count: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Vocabulary Word Schemas ---
class VocabularyWordBase(BaseModel):
    category_id: str
    word: str
    phonetic: Optional[str] = None
    emoji: str = "🌟"
    meaning_vi: Optional[str] = None
    image_url: Optional[str] = None
    custom_audio_url: Optional[str] = None
    example_sentence: Optional[str] = None
    sentence_meaning_vi: Optional[str] = None
    fun_fact: Optional[str] = None
    difficulty_level: str = "easy"
    order_index: int = 0
    is_active: bool = True

class VocabularyWordCreate(VocabularyWordBase):
    id: str

class VocabularyWordUpdate(BaseModel):
    category_id: Optional[str] = None
    word: Optional[str] = None
    phonetic: Optional[str] = None
    emoji: Optional[str] = None
    meaning_vi: Optional[str] = None
    image_url: Optional[str] = None
    custom_audio_url: Optional[str] = None
    example_sentence: Optional[str] = None
    sentence_meaning_vi: Optional[str] = None
    fun_fact: Optional[str] = None
    difficulty_level: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class VocabularyWordResponse(VocabularyWordBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Alphabet Lesson Schemas ---
class AlphabetLessonBase(BaseModel):
    letter: str
    lowercase: str
    word: str
    phonics: str
    emoji: str = "🍎"
    example_sentence: Optional[str] = None
    color: str = "#FF6B6B"
    order_index: int = 0
    is_active: bool = True

class AlphabetLessonCreate(AlphabetLessonBase):
    id: str

class AlphabetLessonUpdate(BaseModel):
    letter: Optional[str] = None
    lowercase: Optional[str] = None
    word: Optional[str] = None
    phonics: Optional[str] = None
    emoji: Optional[str] = None
    example_sentence: Optional[str] = None
    color: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class AlphabetLessonResponse(AlphabetLessonBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Full Content Sync Bundle Schema ---
class ContentSyncBundle(BaseModel):
    version: int
    categories: List[CategoryResponse]
    words: List[VocabularyWordResponse]
    alphabet: List[AlphabetLessonResponse]
    synced_at: str
