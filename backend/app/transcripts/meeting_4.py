MEETING_4 = {
    "meeting_id": "qn234567-89ab-4cde-9012-abcdef123456",
    "meeting_title": "Engineering Sync",
    "date": "2026-04-14",
    "participants": ["Ibrahim", "Hamza", "Ali", "Sara"],
    "transcript": [
        {"timestamp": "11:30:12", "speaker": "Ibrahim", "text": "Align on the scheduler and Notion integration rollout; APScheduler will run the transcript job."},
        {"timestamp": "11:30:35", "speaker": "Hamza", "text": "Scheduler should run periodically and skip meetings already processed (is_summarised/is_vectorized flags)."},
        {"timestamp": "11:30:59", "speaker": "Ali", "text": "I'll map the meetings table and meeting_chunks in SQLAlchemy and ensure pgvector works with embeddings."},
        {"timestamp": "11:31:21", "speaker": "Sara", "text": "I'll validate Notion page structure (summary, action items, decisions) before pushing pages."},
        {"timestamp": "11:31:46", "speaker": "Ibrahim", "text": "Action: add three realistic transcript fixtures under app/transcripts for testing."},
        {"timestamp": "11:32:10", "speaker": "Hamza", "text": "Decision: use OpenRouter summarize function and reuse it for embeddings; keep code simple."}
    ],
}
