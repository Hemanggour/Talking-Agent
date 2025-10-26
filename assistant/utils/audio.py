import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(filename="user_audio.wav", duration=3, fs=24000):
    print(f"Speak now ({duration} seconds)...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print(f"Saved audio to {filename}")
    return filename
