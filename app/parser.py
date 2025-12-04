from typing import List

import nltk
from nltk.tokenize import sent_tokenize


def ensure_nltk_punkt() -> None:
    """Ensure the NLTK punkt tokenizer is available."""
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")


def split_into_sentences(text: str) -> List[str]:
    """Split a transcript into non-empty sentences."""
    text = text.strip()
    if not text:
        return []

    try:
        sentences = sent_tokenize(text)
    except LookupError:
        # Fallback if punkt is missing
        sentences = [s.strip() for s in text.split("\n") if s.strip()]

    return [s.strip() for s in sentences if s.strip()]
