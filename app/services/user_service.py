from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate, ProgressSync

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_profile(self, user: User) -> User:
        return user

    def update_profile(self, user: User, update_data: UserUpdate) -> User:
        return self.user_repo.update_profile(user, update_data)

    def sync_progress(self, user: User, progress_in: ProgressSync) -> User:
        return self.user_repo.sync_progress(user, progress_in)
