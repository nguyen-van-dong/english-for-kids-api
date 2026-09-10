import os
import hashlib
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
import edge_tts
from app.core.config import settings

router = APIRouter()

AUDIO_CACHE_DIR = os.path.abspath(settings.AUDIO_CACHE_DIR)
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

# Recommended Microsoft Neural voices:
# - en-US-AnaNeural: Warm, cheerful child/teen voice (great for kids apps!)
# - en-US-JennyNeural: Warm, gentle female teacher voice
# - en-US-AriaNeural: Confident, expressive female narrator
# - en-US-GuyNeural: Friendly male voice
DEFAULT_VOICE = settings.DEFAULT_TTS_VOICE

@router.get("/tts")
async def generate_speech_audio(
    text: str = Query(..., min_length=1, max_length=300, description="Word or sentence to pronounce"),
    voice: str = Query(DEFAULT_VOICE, description="Microsoft Neural Voice identifier")
):
    """
    Generate or retrieve cached studio HD audio MP3 using Microsoft Neural TTS.
    """
    clean_text = text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Generate deterministic hash for cache key
    cache_key = f"{voice}_{clean_text}".lower()
    file_hash = hashlib.sha256(cache_key.encode('utf-8')).hexdigest()[:20]
    file_name = f"{file_hash}.mp3"
    file_path = os.path.join(AUDIO_CACHE_DIR, file_name)

    # Return cached file if exists
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="audio/mpeg",
            filename=file_name,
            headers={"Cache-Control": "public, max-age=31536000"}
        )

    # Generate new HD audio with edge-tts
    try:
        communicate = edge_tts.Communicate(clean_text, voice=voice)
        await communicate.save(file_path)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Failed to save audio file")

        return FileResponse(
            file_path,
            media_type="audio/mpeg",
            filename=file_name,
            headers={"Cache-Control": "public, max-age=31536000"}
        )
    except Exception as e:
        print(f"Error generating edge-tts audio: {e}")
        raise HTTPException(status_code=500, detail=f"TTS generation error: {str(e)}")
