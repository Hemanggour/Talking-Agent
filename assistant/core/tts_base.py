class TTSBase:
    def __init__(self):
        pass

    def convert_tts(self, text: str):
        raise NotImplementedError("Subclasses must implement the convert_tts method")
