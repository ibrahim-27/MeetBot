MEETING_1 = {
    "meeting_id": "ac67465e-810f-4186-877f-15744514525a",
    "meeting_title": "Project Kickoff",
    "date": "2026-03-18",
    "participants": ["Ibrahim", "Sara", "Ali", "Hamza"],
    "transcript": [
        {"timestamp": "10:00:15", "speaker": "Ibrahim", "text": "Let's build an AI assistant that summarizes transcripts, stores summaries in Notion, and supports RAG chat."},
        {"timestamp": "10:01:18", "speaker": "Ibrahim", "text": "Plan: accept transcript files, run summarization, write to Notion, then chunk and embed for retrieval."},
        {"timestamp": "10:01:35", "speaker": "Hamza", "text": "Chunking needs overlap to keep context and avoid noisy retrieval."},
        {"timestamp": "10:02:02", "speaker": "Sara", "text": "Frontend should be Next.js using a ChatContainer UI and a simple login."},
        {"timestamp": "10:03:05", "speaker": "Ibrahim", "text": "Backend will be FastAPI with async SQLAlchemy and pgvector for embeddings."},
        {"timestamp": "10:05:30", "speaker": "Hamza", "text": "Use OpenRouter for LLM and embeddings initially; keep provider-agnostic design."},
        {"timestamp": "10:06:40", "speaker": "Ibrahim", "text": "Notion will store summary, action items and decisions; keep transcript optional."}
    ],
}