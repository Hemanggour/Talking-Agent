import torch
import whisper

from assistant.config.settings import settings
from assistant.core.stt_base import STTBase


class WhisperSTT(STTBase):
    def __init__(self, device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(settings.WHISPER_MODEL, device=device)

    def convert_stt(self, audio_array):
        result = self.model.transcribe(audio_array, fp16=False)
        spoken_text = result["text"].strip()
        return spoken_text
