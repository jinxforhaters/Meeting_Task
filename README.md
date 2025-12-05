# Meeting Task Extractor (MVP)

A lightweight **Meeting → Tasks** automation engine that converts meeting transcripts (text or audio) into **structured tasks** with:

- ✔ Task description  
- ✔ Assigned team member  
- ✔ Priority (Critical / High / Medium / Low)  
- ✔ Deadline phrase  
- ✔ Dependencies  
- ✔ Reason/explanation  

This MVP is built using:

- **FastAPI** (API layer)  
- **Groq Whisper** (for Speech-to-Text)  
- **Custom rule-based NLP pipeline** (no ML model required)  

The goal is to demonstrate a clean, explainable, working system that transforms real meeting recordings into actionable task lists.

---

## 🚀 Features

### ✓ Extract tasks from raw meeting text  
Send any transcript to `/process-text` and receive structured tasks.

### ✓ Extract tasks from audio (via Groq Whisper)  
Upload `.wav`, `.mp3`, `.m4a`, `.flac`, etc. to `/process-audio`.

### ✓ Rule-based task processing  
Our logic detects:

- Task-like sentences  
- Assigned member based on name mentions  
- Priority from keywords (critical / urgent / high priority / …)  
- Deadline phrases (e.g., “by Friday”, “next week”, “before release”)  
- Task dependencies (e.g., “once Sakshi is done…”)  
- Human-readable reason/explanation  

### ✓ Fully explainable → no machine learning required  
The extraction logic is 100% transparent and editable.

---

## 🛠 Project Structure

Below is the exact folder structure for this project:

Meeting_Task_Extractor/
│
├── app/
│   ├── __init__.py                # Package initializer
│   ├── main.py                    # FastAPI application (routes)
│   ├── models.py                  # Pydantic models for Task and TeamMember
│   ├── parser.py                  # NLTK-based sentence splitter
│   ├── extractor.py               # Rule-based task extraction logic
│   ├── stt.py                     # Groq Whisper STT integration
│
├── sample_data/
│   ├── sample_transcript.txt      # Preloaded example transcript
│   ├── team_members.json          # Example team members list
│   ├── expected_output.json       # Expected output for sample transcript
│   ├── sample1.flac               # Optional: sample audio file for testing
│
├── demo_from_files.py             # Script to run extraction without API
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── .env.example                   # Template for environment variables

Create and Activate a Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Add Your GROQ API Key (.env Setup)

Use the provided .env.example as reference.

Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here


Get your API key from:
👉 https://console.groq.com/keys

Open Swagger API (Interactive Docs)

Open:
👉 http://127.0.0.1:8000/docs

You will see these endpoints:

✔ /process-text

Extract tasks from raw text input.

✔ /process-audio

Upload audio file → Groq Whisper transcription → task extraction. #add your