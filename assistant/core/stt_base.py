class STTBase:
    def __init__(self):
        pass

    def convert_stt(self, audio_path: str):
        raise NotImplementedError("Subclasses must implement the convert_stt method")
