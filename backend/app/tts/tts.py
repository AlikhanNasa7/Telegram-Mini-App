import asyncio
import edge_tts
import os
from pathlib import Path

# Define available voices
VOICES = ["en-US-GuyNeural"]  # Extend as needed

# Directory to store audio files
AUDIO_DIR = Path("audio_files")
AUDIO_DIR.mkdir(exist_ok=True)


async def generate_audio(text: str, voice: str, filename: str) -> Path:
    """
    Generates an audio file from the given text and saves it to AUDIO_DIR.

    Args:
        text (str): The text to convert to speech.
        voice (str): The voice to use for TTS.
        filename (str): The name of the output MP3 file.

    Returns:
        Path: The path to the saved audio file.
    """
    if voice not in VOICES:
        raise ValueError(f"Voice '{voice}' is not supported.")

    output_path = AUDIO_DIR / filename
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))
    return output_path
