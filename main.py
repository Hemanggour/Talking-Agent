from assistant.agents.chat_agent import ChatAgent
from assistant.utils.audio import record_audio
from assistant.utils.stt.whisper_stt import WhisperSTT
from assistant.utils.tts.kokoro_tts import KokoroTTS

chat_agent = ChatAgent()
tts_model = KokoroTTS()
stt_model = WhisperSTT()

audio, _ = record_audio(duration=5)

query = stt_model.convert_stt(audio)
print("You said:", query)

response = chat_agent.invoke(query)
print(f"Response: {response}")

file_path = tts_model.convert_tts(response)
print(file_path)
