import json
import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from .extractor import extract_tasks_from_transcript
from .models import Task, TeamMember
from .parser import ensure_nltk_punkt, split_into_sentences
from .stt import transcribe_audio_file


class ProcessTextRequest(BaseModel):
    transcript: str
    team_members: List[TeamMember]


app = FastAPI(
    title="Meeting Task Extractor",
    description="Convert meeting transcripts into structured tasks.",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    ensure_nltk_punkt()


@app.get("/")
def health_check() -> dict:
    return {
        "status": "ok",
        "endpoints": ["/process-text", "/process-audio"],
    }


@app.post("/process-text", response_model=List[Task])
def process_text(request: ProcessTextRequest) -> List[Task]:
    sentences = split_into_sentences(request.transcript)
    return extract_tasks_from_transcript(sentences, request.team_members)


@app.post("/process-audio", response_model=List[Task])
async def process_audio(
    audio_file: UploadFile = File(...),
    team_members_json: str = Form(...),
) -> List[Task]:
    try:
        raw_list = json.loads(team_members_json)
        team_members = [TeamMember(**item) for item in raw_list]
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid team_members_json: {exc}") from exc

    try:
        suffix = Path(audio_file.filename).suffix if audio_file.filename else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            content = await audio_file.read()
            tmp.write(content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {exc}") from exc

    try:
        transcript = transcribe_audio_file(tmp_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {exc}") from exc

    sentences = split_into_sentences(transcript)
    return extract_tasks_from_transcript(sentences, team_members)
