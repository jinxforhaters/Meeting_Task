import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def transcribe_audio_file(file_path: str) -> str:
    """Transcribe an audio file using Groq Whisper."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)
    audio_path = Path(file_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    with audio_path.open("rb") as f:
        transcription = client.audio.transcriptions.create(
            file=(audio_path.name, f.read()),
            model="whisper-large-v3",
            temperature=0,
            response_format="verbose_json",
        )

    return transcription.text
