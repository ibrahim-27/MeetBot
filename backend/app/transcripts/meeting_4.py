MEETING_4 = {
    "meeting_id": "33333333-3333-4333-8333-333333333333",
    "meeting_title": "Engineering Sync",
    "date": "2026-04-14",
    "participants": ["Ibrahim", "Hamza", "Ali", "Sara"],
    "transcript": [
        {"timestamp": "11:30:12", "speaker": "Ibrahim", "text": "Today we align on scheduler and Notion integration rollout."},
        {"timestamp": "11:30:35", "speaker": "Hamza", "text": "Scheduler should run at midnight and skip already processed meetings."},
        {"timestamp": "11:30:59", "speaker": "Ali", "text": "I will map the meetings table in SQLAlchemy and keep existing schema."},
        {"timestamp": "11:31:21", "speaker": "Sara", "text": "I will validate Notion page structure with summary and action items."},
        {"timestamp": "11:31:46", "speaker": "Ibrahim", "text": "Action item: add three dummy transcripts for test runs."},
        {"timestamp": "11:32:10", "speaker": "Hamza", "text": "Decision: use OpenRouter summarize function without creating a second summarizer."},
    ],
}
