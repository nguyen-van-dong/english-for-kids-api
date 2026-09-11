import os
import hashlib
import edge_tts
from app.core.config import settings
from app.core.exceptions import AppException, AudioGenerationException

class AudioService:
    def __init__(self):
        self.cache_dir = os.path.abspath(settings.AUDIO_CACHE_DIR)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.default_voice = settings.DEFAULT_TTS_VOICE

    async def get_or_generate_audio(
        self,
        text: str,
        voice: str = None,
        rate: str = None,
        volume: str = None,
        pitch: str = None
    ) -> str:
        """
        Get existing cached MP3 or generate HD speech using Microsoft Neural TTS (Edge TTS).
        Returns the absolute file path to the MP3.
        """
        clean_text = text.strip()
        if not clean_text:
            raise AppException("Text cannot be empty", status_code=400)

        selected_voice = voice or self.default_voice
        selected_rate = rate or settings.DEFAULT_TTS_RATE
        selected_volume = volume or settings.DEFAULT_TTS_VOLUME
        selected_pitch = pitch or "+0Hz"

        cache_key = f"{selected_voice}_{selected_rate}_{selected_volume}_{selected_pitch}_{clean_text}".lower()
        file_hash = hashlib.sha256(cache_key.encode("utf-8")).hexdigest()[:20]
        file_name = f"{file_hash}.mp3"
        file_path = os.path.join(self.cache_dir, file_name)

        if os.path.exists(file_path):
            return file_path

        try:
            communicate = edge_tts.Communicate(
                clean_text,
                voice=selected_voice,
                rate=selected_rate,
                volume=selected_volume,
                pitch=selected_pitch
            )
            await communicate.save(file_path)

            if not os.path.exists(file_path):
                raise AudioGenerationException("Failed to save audio file to disk.")

            return file_path
        except AppException:
            raise
        except Exception as e:
            raise AudioGenerationException(f"TTS generation error: {str(e)}")
