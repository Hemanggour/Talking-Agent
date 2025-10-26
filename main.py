from assistant.agents.chat_agent import ChatAgent
from assistant.utils.tts.kokoro_tts import KokoroTTS
# from assistant.utils.stt.whisper_stt import WhisperSTT

# from assistant.utils.audio import record_audio


chat_agent = ChatAgent()
# tts_model = KokoroTTS()
# stt_model = WhisperSTT()

# speech_file_path = record_audio()

# speech_file_path = "user_audio.wav"

# user_query = stt_model.convert_stt(speech_file_path)
# print(f"User Query: {user_query}")

while True:
    user_query = input("Enter your query: ")

    response = chat_agent.invoke(user_query)
    print(f"Response: {response}")

# file_path = tts_model.convert_tts(response)
# print(file_path)
