from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.learning_repository import (
    StudySessionRepository,
    TimelineEventRepository,
    WordProgressRepository,
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.learning_service import LearningService
from app.services.audio_service import AudioService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

# ----------------- Repositories -----------------
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_study_session_repository(db: Session = Depends(get_db)) -> StudySessionRepository:
    return StudySessionRepository(db)

def get_timeline_event_repository(db: Session = Depends(get_db)) -> TimelineEventRepository:
    return TimelineEventRepository(db)

def get_word_progress_repository(db: Session = Depends(get_db)) -> WordProgressRepository:
    return WordProgressRepository(db)

# ----------------- Services -----------------
def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo=user_repo)

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo=user_repo)

def get_learning_service(
    user_repo: UserRepository = Depends(get_user_repository),
    session_repo: StudySessionRepository = Depends(get_study_session_repository),
    timeline_repo: TimelineEventRepository = Depends(get_timeline_event_repository),
    word_repo: WordProgressRepository = Depends(get_word_progress_repository),
) -> LearningService:
    return LearningService(
        user_repo=user_repo,
        session_repo=session_repo,
        timeline_repo=timeline_repo,
        word_repo=word_repo,
    )

def get_audio_service() -> AudioService:
    return AudioService()

# ----------------- Current User -----------------
def get_current_user(
    user_repo: UserRepository = Depends(get_user_repository),
    token: str = Depends(reusable_oauth2)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user
