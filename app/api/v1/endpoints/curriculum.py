from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.curriculum import Category, VocabularyWord, AlphabetLesson
from app.models.cms import ContentVersion
from app.schemas.curriculum import (
    CategoryResponse,
    VocabularyWordResponse,
    AlphabetLessonResponse,
    ContentSyncBundle,
)

router = APIRouter()

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Include inactive categories")
):
    """
    Get all categories for kids learning. Includes word count for each category.
    """
    query = db.query(Category)
    if not include_inactive:
        query = query.filter(Category.is_active == True)
    
    categories = query.order_by(Category.order_index.asc()).all()
    
    results = []
    for cat in categories:
        count = db.query(func.count(VocabularyWord.id)).filter(
            VocabularyWord.category_id == cat.id,
            VocabularyWord.is_active == True
        ).scalar() or 0
        cat_dict = CategoryResponse.from_orm(cat).dict()
        cat_dict["word_count"] = count
        results.append(CategoryResponse(**cat_dict))
    
    return results


@router.get("/categories/{category_id}/words", response_model=List[VocabularyWordResponse])
def get_words_by_category(
    category_id: str,
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False)
):
    """
    Get all active vocabulary words in a specific category.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    query = db.query(VocabularyWord).filter(VocabularyWord.category_id == category_id)
    if not include_inactive:
        query = query.filter(VocabularyWord.is_active == True)

    words = query.order_by(VocabularyWord.order_index.asc()).all()
    return words


@router.get("/words", response_model=List[VocabularyWordResponse])
def get_all_words(
    db: Session = Depends(get_db),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: easy, medium, hard"),
    include_inactive: bool = Query(False)
):
    """
    Get all vocabulary words across all categories.
    """
    query = db.query(VocabularyWord)
    if not include_inactive:
        query = query.filter(VocabularyWord.is_active == True)
    if difficulty:
        query = query.filter(VocabularyWord.difficulty_level == difficulty)

    words = query.order_by(VocabularyWord.order_index.asc()).all()
    return words


@router.get("/alphabet", response_model=List[AlphabetLessonResponse])
def get_alphabet_lessons(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False)
):
    """
    Get 26 alphabet phonics lessons.
    """
    query = db.query(AlphabetLesson)
    if not include_inactive:
        query = query.filter(AlphabetLesson.is_active == True)

    lessons = query.order_by(AlphabetLesson.order_index.asc()).all()
    return lessons


@router.get("/sync-bundle", response_model=ContentSyncBundle)
def get_curriculum_sync_bundle(db: Session = Depends(get_db)):
    """
    Get complete active curriculum bundle in a single fast call for mobile app offline storage.
    """
    version_row = db.query(ContentVersion).filter(ContentVersion.id == "curriculum").first()
    version = version_row.version_number if version_row else 1

    categories = db.query(Category).filter(Category.is_active == True).order_by(Category.order_index.asc()).all()
    category_responses = []
    for cat in categories:
        count = db.query(func.count(VocabularyWord.id)).filter(
            VocabularyWord.category_id == cat.id,
            VocabularyWord.is_active == True
        ).scalar() or 0
        cat_dict = CategoryResponse.from_orm(cat).dict()
        cat_dict["word_count"] = count
        category_responses.append(CategoryResponse(**cat_dict))

    words = db.query(VocabularyWord).filter(VocabularyWord.is_active == True).order_by(VocabularyWord.order_index.asc()).all()
    alphabet = db.query(AlphabetLesson).filter(AlphabetLesson.is_active == True).order_by(AlphabetLesson.order_index.asc()).all()

    return ContentSyncBundle(
        version=version,
        categories=category_responses,
        words=words,
        alphabet=alphabet,
        synced_at=datetime.utcnow().isoformat()
    )
