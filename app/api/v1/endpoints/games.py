from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.games import QuizQuestion, SpellingWord, SpeakingChallenge
from app.models.cms import ContentVersion
from app.schemas.games import (
    QuizQuestionResponse,
    SpellingWordResponse,
    SpeakingChallengeResponse,
    GamesSyncBundle,
)

router = APIRouter()

@router.get("/quizzes", response_model=List[QuizQuestionResponse])
def get_quiz_questions(
    db: Session = Depends(get_db),
    level: Optional[str] = Query(None, description="easy, medium, hard"),
    category_id: Optional[str] = Query(None),
    include_inactive: bool = Query(False)
):
    """
    Get active quiz questions with optional level and category filters.
    """
    query = db.query(QuizQuestion)
    if not include_inactive:
        query = query.filter(QuizQuestion.is_active == True)
    if level:
        query = query.filter(QuizQuestion.level == level)
    if category_id:
        query = query.filter(QuizQuestion.category_id == category_id)

    quizzes = query.order_by(QuizQuestion.order_index.asc()).all()
    return quizzes


@router.get("/spelling", response_model=List[SpellingWordResponse])
def get_spelling_words(
    db: Session = Depends(get_db),
    level: Optional[str] = Query(None, description="easy, medium, hard"),
    include_inactive: bool = Query(False)
):
    """
    Get active spelling game words.
    """
    query = db.query(SpellingWord)
    if not include_inactive:
        query = query.filter(SpellingWord.is_active == True)
    if level:
        query = query.filter(SpellingWord.level == level)

    words = query.order_by(SpellingWord.order_index.asc()).all()
    return words


@router.get("/speaking", response_model=List[SpeakingChallengeResponse])
def get_speaking_challenges(
    db: Session = Depends(get_db),
    level: Optional[str] = Query(None, description="easy, medium, hard"),
    include_inactive: bool = Query(False)
):
    """
    Get active AI speaking challenges.
    """
    query = db.query(SpeakingChallenge)
    if not include_inactive:
        query = query.filter(SpeakingChallenge.is_active == True)
    if level:
        query = query.filter(SpeakingChallenge.level == level)

    challenges = query.order_by(SpeakingChallenge.order_index.asc()).all()
    return challenges


@router.get("/sync-bundle", response_model=GamesSyncBundle)
def get_games_sync_bundle(db: Session = Depends(get_db)):
    """
    Get all active games data (Quizzes, Spelling, Speaking) in a single bundle for offline caching.
    """
    version_row = db.query(ContentVersion).filter(ContentVersion.id == "games").first()
    version = version_row.version_number if version_row else 1

    quizzes = db.query(QuizQuestion).filter(QuizQuestion.is_active == True).order_by(QuizQuestion.order_index.asc()).all()
    spelling = db.query(SpellingWord).filter(SpellingWord.is_active == True).order_by(SpellingWord.order_index.asc()).all()
    speaking = db.query(SpeakingChallenge).filter(SpeakingChallenge.is_active == True).order_by(SpeakingChallenge.order_index.asc()).all()

    return GamesSyncBundle(
        version=version,
        quizzes=quizzes,
        spelling_words=spelling,
        speaking_challenges=speaking,
        synced_at=datetime.utcnow().isoformat()
    )
