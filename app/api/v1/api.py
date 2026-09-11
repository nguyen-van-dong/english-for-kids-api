from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, audio, learning, curriculum, games, cms, admin_content

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(cms.router, prefix="/cms", tags=["cms"])
api_router.include_router(admin_content.router, prefix="/admin", tags=["admin"])

