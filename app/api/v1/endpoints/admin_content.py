from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.curriculum import Category, VocabularyWord, AlphabetLesson
from app.models.games import QuizQuestion, SpellingWord, SpeakingChallenge
from app.models.gamification import AchievementBadge, AvatarCharacter, StickerItem
from app.models.cms import HomeBanner, DailyQuest, AppSetting, ContentVersion

from app.schemas.curriculum import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    VocabularyWordCreate, VocabularyWordUpdate, VocabularyWordResponse,
    AlphabetLessonCreate, AlphabetLessonUpdate, AlphabetLessonResponse
)
from app.schemas.games import (
    QuizQuestionCreate, QuizQuestionUpdate, QuizQuestionResponse,
    SpellingWordCreate, SpellingWordUpdate, SpellingWordResponse,
    SpeakingChallengeCreate, SpeakingChallengeUpdate, SpeakingChallengeResponse
)
from app.schemas.cms import (
    HomeBannerCreate, HomeBannerUpdate, HomeBannerResponse,
    DailyQuestCreate, DailyQuestUpdate, DailyQuestResponse,
    AchievementBadgeCreate, AchievementBadgeUpdate, AchievementBadgeResponse,
    AvatarCharacterCreate, AvatarCharacterUpdate, AvatarCharacterResponse,
    StickerItemCreate, StickerItemUpdate, StickerItemResponse,
    AppSettingCreate, AppSettingUpdate, AppSettingResponse
)

router = APIRouter()

def bump_version(db: Session, module_id: str):
    version_row = db.query(ContentVersion).filter(ContentVersion.id == module_id).first()
    if version_row:
        version_row.version_number += 1
    else:
        version_row = ContentVersion(id=module_id, version_number=1)
        db.add(version_row)
    db.commit()


# ==============================================================================
# CATEGORIES CRUD
# ==============================================================================
@router.post("/categories", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(Category).filter(Category.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Category ID already exists")
    category = Category(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    bump_version(db, "curriculum")
    return category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    bump_version(db, "curriculum")
    return category

@router.delete("/categories/{category_id}")
def delete_category(category_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    bump_version(db, "curriculum")
    return {"success": True, "message": f"Category {category_id} deleted"}


# ==============================================================================
# VOCABULARY WORDS CRUD
# ==============================================================================
@router.post("/words", response_model=VocabularyWordResponse)
def create_word(payload: VocabularyWordCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(VocabularyWord).filter(VocabularyWord.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Word ID already exists")
    word = VocabularyWord(**payload.dict())
    db.add(word)
    db.commit()
    db.refresh(word)
    bump_version(db, "curriculum")
    return word

@router.put("/words/{word_id}", response_model=VocabularyWordResponse)
def update_word(word_id: str, payload: VocabularyWordUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    word = db.query(VocabularyWord).filter(VocabularyWord.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(word, field, value)
    db.commit()
    db.refresh(word)
    bump_version(db, "curriculum")
    return word

@router.delete("/words/{word_id}")
def delete_word(word_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    word = db.query(VocabularyWord).filter(VocabularyWord.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    db.delete(word)
    db.commit()
    bump_version(db, "curriculum")
    return {"success": True, "message": f"Word {word_id} deleted"}


# ==============================================================================
# ALPHABET LESSONS CRUD
# ==============================================================================
@router.post("/alphabet", response_model=AlphabetLessonResponse)
def create_alphabet_lesson(payload: AlphabetLessonCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(AlphabetLesson).filter(AlphabetLesson.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Alphabet Lesson ID already exists")
    lesson = AlphabetLesson(**payload.dict())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    bump_version(db, "curriculum")
    return lesson

@router.put("/alphabet/{lesson_id}", response_model=AlphabetLessonResponse)
def update_alphabet_lesson(lesson_id: str, payload: AlphabetLessonUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    lesson = db.query(AlphabetLesson).filter(AlphabetLesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Alphabet Lesson not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(lesson, field, value)
    db.commit()
    db.refresh(lesson)
    bump_version(db, "curriculum")
    return lesson

@router.delete("/alphabet/{lesson_id}")
def delete_alphabet_lesson(lesson_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    lesson = db.query(AlphabetLesson).filter(AlphabetLesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Alphabet Lesson not found")
    db.delete(lesson)
    db.commit()
    bump_version(db, "curriculum")
    return {"success": True, "message": f"Alphabet Lesson {lesson_id} deleted"}


# ==============================================================================
# QUIZ QUESTIONS CRUD
# ==============================================================================
@router.post("/quizzes", response_model=QuizQuestionResponse)
def create_quiz_question(payload: QuizQuestionCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(QuizQuestion).filter(QuizQuestion.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Quiz ID already exists")
    quiz = QuizQuestion(**payload.dict())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    bump_version(db, "games")
    return quiz

@router.put("/quizzes/{quiz_id}", response_model=QuizQuestionResponse)
def update_quiz_question(quiz_id: str, payload: QuizQuestionUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    quiz = db.query(QuizQuestion).filter(QuizQuestion.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz Question not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(quiz, field, value)
    db.commit()
    db.refresh(quiz)
    bump_version(db, "games")
    return quiz

@router.delete("/quizzes/{quiz_id}")
def delete_quiz_question(quiz_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    quiz = db.query(QuizQuestion).filter(QuizQuestion.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz Question not found")
    db.delete(quiz)
    db.commit()
    bump_version(db, "games")
    return {"success": True, "message": f"Quiz Question {quiz_id} deleted"}


# ==============================================================================
# SPELLING & SPEAKING CRUD
# ==============================================================================
@router.post("/spelling", response_model=SpellingWordResponse)
def create_spelling_word(payload: SpellingWordCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(SpellingWord).filter(SpellingWord.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Spelling Word ID already exists")
    sp = SpellingWord(**payload.dict())
    db.add(sp)
    db.commit()
    db.refresh(sp)
    bump_version(db, "games")
    return sp

@router.put("/spelling/{spelling_id}", response_model=SpellingWordResponse)
def update_spelling_word(spelling_id: str, payload: SpellingWordUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    sp = db.query(SpellingWord).filter(SpellingWord.id == spelling_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Spelling Word not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(sp, field, value)
    db.commit()
    db.refresh(sp)
    bump_version(db, "games")
    return sp

@router.delete("/spelling/{spelling_id}")
def delete_spelling_word(spelling_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    sp = db.query(SpellingWord).filter(SpellingWord.id == spelling_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Spelling Word not found")
    db.delete(sp)
    db.commit()
    bump_version(db, "games")
    return {"success": True, "message": f"Spelling Word {spelling_id} deleted"}


@router.post("/speaking", response_model=SpeakingChallengeResponse)
def create_speaking_challenge(payload: SpeakingChallengeCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(SpeakingChallenge).filter(SpeakingChallenge.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Speaking Challenge ID already exists")
    spk = SpeakingChallenge(**payload.dict())
    db.add(spk)
    db.commit()
    db.refresh(spk)
    bump_version(db, "games")
    return spk

@router.put("/speaking/{challenge_id}", response_model=SpeakingChallengeResponse)
def update_speaking_challenge(challenge_id: str, payload: SpeakingChallengeUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    spk = db.query(SpeakingChallenge).filter(SpeakingChallenge.id == challenge_id).first()
    if not spk:
        raise HTTPException(status_code=404, detail="Speaking Challenge not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(spk, field, value)
    db.commit()
    db.refresh(spk)
    bump_version(db, "games")
    return spk

@router.delete("/speaking/{challenge_id}")
def delete_speaking_challenge(challenge_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    spk = db.query(SpeakingChallenge).filter(SpeakingChallenge.id == challenge_id).first()
    if not spk:
        raise HTTPException(status_code=404, detail="Speaking Challenge not found")
    db.delete(spk)
    db.commit()
    bump_version(db, "games")
    return {"success": True, "message": f"Speaking Challenge {challenge_id} deleted"}


# ==============================================================================
# BANNERS & DAILY QUESTS CRUD
# ==============================================================================
@router.post("/banners", response_model=HomeBannerResponse)
def create_home_banner(payload: HomeBannerCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    if db.query(HomeBanner).filter(HomeBanner.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Banner ID already exists")
    banner = HomeBanner(**payload.dict())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    bump_version(db, "cms")
    return banner

@router.put("/banners/{banner_id}", response_model=HomeBannerResponse)
def update_home_banner(banner_id: str, payload: HomeBannerUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    banner = db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(banner, field, value)
    db.commit()
    db.refresh(banner)
    bump_version(db, "cms")
    return banner

@router.delete("/banners/{banner_id}")
def delete_home_banner(banner_id: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    banner = db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    db.delete(banner)
    db.commit()
    bump_version(db, "cms")
    return {"success": True, "message": f"Banner {banner_id} deleted"}


# ==============================================================================
# APP SETTINGS CRUD
# ==============================================================================
@router.post("/settings", response_model=AppSettingResponse)
def set_app_setting(payload: AppSettingCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    setting = db.query(AppSetting).filter(AppSetting.config_key == payload.config_key).first()
    if setting:
        setting.config_value = payload.config_value
        setting.data_type = payload.data_type
        setting.description = payload.description
        setting.is_public = payload.is_public
    else:
        setting = AppSetting(**payload.dict())
        db.add(setting)
    db.commit()
    db.refresh(setting)
    bump_version(db, "cms")
    return setting

@router.delete("/settings/{config_key}")
def delete_app_setting(config_key: str, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    setting = db.query(AppSetting).filter(AppSetting.config_key == config_key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="App Setting not found")
    db.delete(setting)
    db.commit()
    bump_version(db, "cms")
    return {"success": True, "message": f"Setting {config_key} deleted"}
