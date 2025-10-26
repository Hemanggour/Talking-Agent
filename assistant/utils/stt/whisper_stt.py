import whisper
import torch
from assistant.core.stt_base import STTBase


class WhisperSTT(STTBase):
    def __init__(self, device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = whisper.load_model("tiny", device=device)

    def convert_stt(self, audio_file):
        result = self.model.transcribe(audio_file)
        spoken_text = result["text"].strip()
        return spoken_text
