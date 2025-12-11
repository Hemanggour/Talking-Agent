# M-AI: Multimodal AI Assistant

A sophisticated conversational AI assistant that combines multiple AI services to create an interactive dialogue experience. The system leverages speech-to-text (STT), large language models (LLM), and text-to-speech (TTS) to enable natural voice-based conversations with an intelligent, personality-driven assistant.

## Features

- **Voice Input**: Record audio directly and transcribe using OpenAI's Whisper model
- **Intelligent Responses**: Powered by Google's Gemini 2.0 Flash for conversational AI
- **Multiple TTS Options**: 
  - Gemini TTS for Google-powered speech synthesis
  - Kokoro TTS (82M model) for efficient local speech generation
- **Conversation Memory**: Built-in conversation history using LangGraph for contextual awareness
- **Personality-Driven**: Interact with "Isabella," a charming AI assistant with a distinct personality
- **Device-Agnostic**: Automatic GPU/CPU detection and optimization

## Project Structure

```
M-AI/
├── main.py                          # Entry point for the application
├── requirements.txt                 # Python dependencies
├── qa.bat                          # Quality assurance script (linting & formatting)
├── assistant/
│   ├── __init__.py
│   ├── agents/
│   │   └── chat_agent.py           # Core chat agent using LangGraph
│   ├── config/
│   │   └── settings.py             # Application configuration & environment variables
│   ├── core/
│   │   ├── agent_base.py           # Base class for agents
│   │   ├── stt_base.py             # Base class for STT implementations
│   │   └── tts_base.py             # Base class for TTS implementations
│   └── utils/
│       ├── audio.py                # Audio recording utilities
│       ├── prompts/
│       │   └── system_prompts.py   # System prompts for personality & behavior
│       ├── stt/
│       │   └── whisper_stt.py      # OpenAI Whisper STT implementation
│       └── tts/
│           ├── gemini_tts/         # Google Gemini TTS implementation
│           └── kokoro_tts/         # Kokoro TTS implementation
├── docs/
│   └── ex.py                       # Example/documentation scripts
└── output/
    └── kokoro/                     # Generated audio output directory
        ├── af_kore/                # African Kore voice output
        └── am_adam/                # American Adam voice output
```

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd c:\Users\lenovo\Code\M-AI
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```
   WHISPER_MODEL=tiny
   LANGUAGE_MODEL=gemini-2.0-flash
   LANGUAGE_MODEL_PROVIDER=google_genai
   ```

   Optional configurations:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

### Basic Example

Run the main application:
```bash
python main.py
```

This will:
1. Record 5 seconds of audio from your microphone
2. Transcribe the audio using Whisper STT
3. Process the transcription through the chat agent
4. Generate a response and convert it to speech using TTS
5. Save the audio output

### Using Different Components

**With Kokoro TTS**:
```python
from assistant.agents.chat_agent import ChatAgent
from assistant.utils.tts.kokoro_tts import KokoroTTS

chat_agent = ChatAgent()
tts_model = KokoroTTS()

response = chat_agent.invoke("How are you?")
audio_file = tts_model.convert_tts(response)
```

**With Gemini TTS**:
```python
from assistant.utils.tts.gemini_tts import GeminiTTS

tts_model = GeminiTTS()
audio_file = tts_model.convert_tts("Hello, how can I help you?")
```

## Key Components

### ChatAgent (`assistant/agents/chat_agent.py`)
- Uses LangGraph for conversation state management
- Maintains conversation history with built-in memory checkpointer
- Integrates with Google's Gemini LLM
- Generates context-aware responses with personality

### Whisper STT (`assistant/utils/stt/whisper_stt.py`)
- OpenAI's Whisper model for speech-to-text conversion
- Supports configurable model sizes (tiny, base, small, medium, large)
- Automatic GPU/CPU device selection

### TTS Systems
- **Kokoro TTS**: Lightweight (82M parameters), supports multiple voices, local execution
- **Gemini TTS**: High-quality Google-powered synthesis with advanced voice options

### Audio Utilities (`assistant/utils/audio.py`)
- Real-time microphone recording
- Audio normalization and preprocessing
- Configurable sample rate and duration

## Configuration

All settings are managed through `assistant/config/settings.py`:

- `WHISPER_MODEL`: Model size for speech recognition (default: "tiny")
- `LANGUAGE_MODEL`: LLM model identifier (default: "gemini-2.0-flash")
- `LANGUAGE_MODEL_PROVIDER`: Provider for the LLM (default: "google_genai")
- `KOKORO_MODEL_CONFIG`: Configuration for Kokoro TTS
- `DEFAULT_VOICE`: Default voice for TTS (default: "af_kore")
- `DEFAULT_OUTPUT_DIR`: Output directory for generated audio files

## Development

### Code Quality Tools

The project includes automated code quality checks via `qa.bat`:

```bash
qa.bat
```

This runs:
- **isort**: Import sorting for consistency
- **black**: Code formatting (100 character line length)
- **flake8**: Style checking and linting

### Project Dependencies

Key dependencies include:
- `langchain`: LLM orchestration and chain management
- `langgraph`: Stateful conversation management
- `google-genai`: Google's generative AI integration
- `openai-whisper`: Speech-to-text engine
- `kokoro`: Efficient TTS model
- `sounddevice`: Audio input/output
- `torch`: Deep learning framework

## Assistant Personality

The assistant "Isabella" is configured with a distinct personality:
- **Role**: The user's best friend with a charming and flirty personality
- **Vibe**: Playful, teasing, warm, and emotionally intelligent
- **Goals**: Keep conversations light, fun, and engaging while maintaining respect and emotional awareness

This is defined in `assistant/utils/prompts/system_prompts.py` and can be customized.

## API Keys

To use Google's Generative AI models, you'll need to set the `GOOGLE_API_KEY`:

```bash
$env:GOOGLE_API_KEY = "your_api_key_here"
```

Or add it to your `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

## Output Files

Generated audio files are saved to:
```
./output/kokoro/{voice_name}/
```

Example paths:
- `./output/kokoro/af_kore/` - African Kore voice outputs
- `./output/kokoro/am_adam/` - American Adam voice outputs

## Troubleshooting

### Audio Recording Issues
- Ensure your microphone is properly connected and configured
- Check microphone permissions in Windows settings
- Verify `sounddevice` is installed correctly

### Model Download Issues
- First run may take time to download models (Whisper, Kokoro, etc.)
- Ensure internet connectivity during model initialization
- Check disk space (models can be several gigabytes)

### GPU Acceleration
- CUDA-compatible GPU will be automatically used if available
- Falls back to CPU automatically if CUDA is not detected
- Whisper and Kokoro both support GPU acceleration

## Future Enhancements

- [ ] Web interface for the chat assistant
- [ ] Multi-language support
- [ ] Custom voice training
- [ ] Conversation logging and analytics
- [ ] Integration with more TTS providers
- [ ] Advanced emotion detection from voice

## Contact & Support

For issues, questions, or improvements, please refer to the project repository.
