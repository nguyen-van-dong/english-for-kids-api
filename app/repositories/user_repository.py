from datetime import datetime
from typing import Optional, List, Set
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserUpdate, ProgressSync

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email.strip().lower()).first()

    def create_user(
        self,
        email: str,
        hashed_password: str,
        parent_name: str,
        child_name: str,
        child_age: int,
        avatar: str,
        verification_code: str,
        verification_code_expires_at: datetime,
    ) -> User:
        user = User(
            email=email.strip().lower(),
            hashed_password=hashed_password,
            parent_name=parent_name or "",
            child_name=child_name,
            child_age=child_age,
            avatar=avatar or "🦁",
            is_verified=False,
            verification_code=verification_code,
            verification_code_expires_at=verification_code_expires_at,
            stars=10,
            streak_days=1,
            mastered_words=[],
            completed_categories=[],
            quiz_high_score=0,
            total_study_minutes=0,
        )
        return self.create(user)

    def update_verification_code(
        self,
        user: User,
        verification_code: str,
        expires_at: datetime
    ) -> User:
        user.verification_code = verification_code
        user.verification_code_expires_at = expires_at
        return self.save(user)

    def mark_email_verified(self, user: User) -> User:
        user.is_verified = True
        user.verification_code = None
        user.verification_code_expires_at = None
        return self.save(user)

    def update_profile(self, user: User, update_data: UserUpdate) -> User:
        if update_data.parent_name is not None:
            user.parent_name = update_data.parent_name
        if update_data.child_name is not None:
            user.child_name = update_data.child_name
        if update_data.child_age is not None:
            user.child_age = update_data.child_age
        if update_data.avatar is not None:
            user.avatar = update_data.avatar
        return self.save(user)

    def sync_progress(self, user: User, progress_in: ProgressSync) -> User:
        if progress_in.stars is not None:
            user.stars = max(user.stars, progress_in.stars)
        if progress_in.streak_days is not None:
            user.streak_days = max(user.streak_days, progress_in.streak_days)
        if progress_in.last_active_date is not None:
            user.last_active_date = progress_in.last_active_date
        if progress_in.mastered_words is not None:
            existing: Set[str] = set(user.mastered_words or [])
            user.mastered_words = list(existing.union(set(progress_in.mastered_words)))
        if progress_in.completed_categories is not None:
            existing_cat: Set[str] = set(user.completed_categories or [])
            user.completed_categories = list(existing_cat.union(set(progress_in.completed_categories)))
        if progress_in.quiz_high_score is not None:
            user.quiz_high_score = max(user.quiz_high_score, progress_in.quiz_high_score)
        return self.save(user)

    def update_total_study_minutes(self, user: User, minutes: int) -> User:
        user.total_study_minutes = max(user.total_study_minutes or 0, minutes)
        return self.save(user)
