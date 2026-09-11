import os
from fastapi import APIRouter, Query, Depends
from fastapi.responses import FileResponse

from app.api.deps import get_audio_service
from app.core.config import settings
from app.services.audio_service import AudioService

router = APIRouter()

DEFAULT_VOICE = settings.DEFAULT_TTS_VOICE

@router.get("/tts")
async def generate_speech_audio(
    text: str = Query(..., min_length=1, max_length=300, description="Word or sentence to pronounce"),
    voice: str = Query(DEFAULT_VOICE, description="Microsoft Neural Voice identifier"),
    audio_service: AudioService = Depends(get_audio_service)
):
    """
    Generate or retrieve cached studio HD audio MP3 using Microsoft Neural TTS.
    """
    file_path = await audio_service.get_or_generate_audio(text=text, voice=voice)
    file_name = os.path.basename(file_path)

    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=file_name,
        headers={"Cache-Control": "public, max-age=31536000"}
    )
