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

