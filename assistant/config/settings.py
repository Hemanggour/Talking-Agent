import json
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")

        self.LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL", "gemini-2.0-flash")
        self.LANGUAGE_MODEL_PROVIDER = os.getenv(
            "LANGUAGE_MODEL_PROVIDER", "google_genai"
        )

        self.KOKORO_MODEL_CONFIG = self.load_model_config(
            "./assistant/utils/tts/kokoro_tts/kokoro_config.json"
        )
        # self.DEFAULT_VOICE = self.KOKORO_MODEL_CONFIG.get("defaults").get("voice")
        self.DEFAULT_VOICE = "af_kore"
        self.DEFAULT_OUTPUT_DIR = f"./output/kokoro/{self.DEFAULT_VOICE}"

    def load_model_config(self, path: str):
        with open(path, "r") as f:
            config = json.load(f)
            return config


settings = Settings()
