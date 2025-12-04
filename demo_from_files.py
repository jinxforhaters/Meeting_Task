import json
from pathlib import Path

from app.extractor import extract_tasks_from_transcript
from app.models import TeamMember
from app.parser import ensure_nltk_punkt, split_into_sentences


def main() -> None:
    base = Path(__file__).parent
    transcript_path = base / "sample_data" / "sample_transcript.txt"
    members_path = base / "sample_data" / "team_members.json"

    transcript = transcript_path.read_text(encoding="utf-8")
    raw_members = json.loads(members_path.read_text(encoding="utf-8"))
    team_members = [TeamMember(**m) for m in raw_members]

    ensure_nltk_punkt()
    sentences = split_into_sentences(transcript)
    tasks = extract_tasks_from_transcript(sentences, team_members)

    print("Sentences:")
    for s in sentences:
        print("-", s)

    print("\nTasks:")
    for t in tasks:
        print(json.dumps(t.model_dump(), indent=2))


if __name__ == "__main__":
    main()
