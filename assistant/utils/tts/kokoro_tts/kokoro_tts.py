import uuid

from kokoro import KPipeline
import soundfile as sf
import numpy as np
import torch
import os

from assistant.core.tts_base import TTSBase
from assistant.config.settings import settings


class KokoroTTS(TTSBase):
    def __init__(self, device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        # Ensure output directory exists
        os.makedirs(settings.DEFAULT_OUTPUT_DIR, exist_ok=True)

        self.pipeline = KPipeline(
            lang_code=settings.KOKORO_MODEL_CONFIG.get("defaults").get("language_code"),
            repo_id=settings.KOKORO_MODEL_CONFIG.get("repo_id"),
            device=device,
        )

    def convert_tts(
        self,
        text: str,
        voice: str = settings.DEFAULT_VOICE,
        output_file: str = None,
        **kwargs,
    ):
        """
        Generate speech using Kokoro-82M TTS.
        
        Args:
            text (str): The input text to be converted to speech
            voice (str): Voice to use for synthesis (default: current voice)
            output_file (str, optional): Output WAV file path. If None, a temporary file is created.
            **kwargs: Additional arguments
            
        Returns:
            str: Path to the generated audio file
            
        Raises:
            ValueError: If no voice is selected or audio generation fails
        """
        if not voice and not hasattr(self, 'voice'):
            raise ValueError("No voice selected. Please select a voice first.")
            
        voice_to_use = voice if voice is not None else getattr(self, 'voice', None)
        
        if not output_file:
            os.makedirs(settings.DEFAULT_OUTPUT_DIR, exist_ok=True)
            output_file = os.path.join(settings.DEFAULT_OUTPUT_DIR, f"{uuid.uuid4()}.wav")
        else:
            os.makedirs(os.path.dirname(os.path.abspath(output_file)) or ".", exist_ok=True)
        
        print(f"Generating speech with voice: {voice_to_use}")
        
        try:
            # Generate audio chunks
            generator = self.pipeline(text, voice=voice_to_use)
            audio_chunks = []
            
            for i, (graphemes, phonemes, audio) in enumerate(generator):
                print(f"Processing chunk {i+1}...")
                print(f"Graphemes: {graphemes}")
                print(f"Phonemes: {phonemes}")
                
                if audio is not None:
                    # Convert to numpy array if needed
                    if not isinstance(audio, np.ndarray):
                        audio = np.array(audio)
                    
                    # Ensure proper shape (samples, channels)
                    if len(audio.shape) == 1:
                        audio = audio.reshape(-1, 1)
                    elif len(audio.shape) > 2:
                        audio = audio.reshape(-1, audio.shape[-1])
                        
                    audio_chunks.append(audio)
            
            if not audio_chunks:
                raise ValueError("No audio was generated")
            
            # Combine all audio chunks
            combined_audio = np.concatenate(audio_chunks, axis=0)
            
            # Ensure proper audio format (mono, float32)
            if combined_audio.dtype != np.float32:
                combined_audio = combined_audio.astype(np.float32)
            
            # Normalize audio to prevent clipping
            max_val = np.max(np.abs(combined_audio))
            if max_val > 0:
                combined_audio = combined_audio / max(1.0, max_val)
            
            # Save the audio file
            sf.write(output_file, combined_audio, 24000)
            
            # Verify the file was created successfully
            if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
                raise IOError("Failed to write audio file")
                
            print(f"Successfully saved audio to {output_file}")
            return output_file
            
        except Exception as e:
            # Clean up partial file if it exists
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except:
                    pass
            raise ValueError(f"Error generating speech: {str(e)}")


    def multi_speak(self, paragraph_parts, output_file=settings.DEFAULT_OUTPUT_DIR, **kwargs):
        """
        Generate speech with multiple voices and emotional markup.
        
        Args:
            paragraph_parts (list of dict): Each dict has {"text": str, "voice": str}
            output_file (str): Output WAV file path
        """
        audios = []

        for part in paragraph_parts:
            text = part["text"]
            voice = part.get("voice", settings.DEFAULT_VOICE)

            generator = self.pipeline(text, voice=voice)

            for _, _, audio in generator:
                audios.append(audio)

        # Concatenate all audio parts
        final_audio = np.concatenate(audios, axis=0)
        sf.write(output_file, final_audio, 24000)

        return output_file


    def select_voice(self, voice: str, **kwargs):
        """
        Select a voice for the TTS model.
        
        Args:
            voice (str): The voice ID to select (e.g., 'am_adam', 'af_nicole')
            **kwargs: Additional arguments (e.g., language_code for validation)
            
        Returns:
            bool: True if voice was set successfully, False otherwise
            
        Raises:
            ValueError: If the specified voice is not found
        """
        if not voice:
            raise ValueError("Voice cannot be empty")
            
        # Get all available voices
        all_voices = []
        voices_by_lang = self.get_voices()
        
        for lang_voices in voices_by_lang.values():
            if isinstance(lang_voices, list):
                all_voices.extend(lang_voices)
        
        # Check if voice exists
        if voice not in all_voices:
            raise ValueError(
                f"Voice '{voice}' not found. Available voices: {all_voices}"
            )
        
        # Set the voice
        self.voice = voice
        
        # Update the pipeline with the new voice if needed
        if hasattr(self, 'pipeline') and hasattr(self.pipeline, 'voice'):
            self.pipeline.voice = voice
            
        return True


    @staticmethod
    def get_languages(**kwargs):
        language_codes = settings.KOKORO_MODEL_CONFIG.get("languages")
        languages = []

        for code in language_codes:
            languages.append(language_codes.get(code).get("name"))
        
        return languages


    @classmethod
    def get_voices(cls, **kwargs):
        """
        Get available voices, optionally filtered by language code.
        
        Args:
            language_code (str, optional): Language code to filter voices
            
        Returns:
            dict: If no language_code is provided, returns a dict with language names as keys
                  and lists of voices as values.
                  If language_code is provided, returns a list of voices for that language.
        """
        languages = settings.KOKORO_MODEL_CONFIG.get("languages", {})
        
        # If language_code is provided, return just the voices for that language
        if "language_code" in kwargs and kwargs["language_code"] is not None:
            lang_code = kwargs["language_code"]
            if lang_code in languages:
                return languages[lang_code].get("voices", [])
            return []
        
        # Otherwise return all voices grouped by language
        voices = {}
        for lang_code, lang_data in languages.items():
            lang_name = lang_data.get("name", f"Language {lang_code}")
            voices[lang_name] = lang_data.get("voices", [])
            
        return voices
