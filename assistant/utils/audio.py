import numpy as np
import sounddevice as sd


def record_audio(duration=3, fs=24000):
    print(f"Speak now ({duration} seconds)...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio = recording.flatten().astype(np.float32)
    audio /= np.max(np.abs(audio))
    return audio, fs
