from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True) # e.g. 'animals', 'fruits'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, default="paw", nullable=False) # icon identifier e.g. 'paw', 'nutrition'
    color = Column(String, default="#FF9671", nullable=False)
    light_color = Column(String, default="#FFF0EB", nullable=False)
    age_min = Column(Integer, default=3)
    age_max = Column(Integer, default=10)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    is_free = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    words = relationship("VocabularyWord", back_populates="category", cascade="all, delete-orphan", order_by="VocabularyWord.order_index")


class VocabularyWord(Base):
    __tablename__ = "vocabulary_words"

    id = Column(String, primary_key=True, index=True) # e.g. 'anim_1', 'fruit_3'
    category_id = Column(String, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    word = Column(String, nullable=False, index=True)
    phonetic = Column(String, nullable=True)
    emoji = Column(String, default="🌟", nullable=False)
    meaning_vi = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    custom_audio_url = Column(String, nullable=True)
    example_sentence = Column(Text, nullable=True)
    sentence_meaning_vi = Column(Text, nullable=True)
    fun_fact = Column(Text, nullable=True)
    difficulty_level = Column(String, default="easy", index=True) # 'easy', 'medium', 'hard'
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="words")


class AlphabetLesson(Base):
    __tablename__ = "alphabet_lessons"

    id = Column(String, primary_key=True, index=True) # e.g. 'a', 'b', 'c'
    letter = Column(String, nullable=False, index=True) # e.g. 'A'
    lowercase = Column(String, nullable=False) # e.g. 'a'
    word = Column(String, nullable=False) # e.g. 'Apple'
    phonics = Column(String, nullable=False) # e.g. '/æ/'
    emoji = Column(String, default="🍎", nullable=False)
    example_sentence = Column(Text, nullable=True)
    color = Column(String, default="#FF6B6B", nullable=False)
    order_index = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
