MEETING_5 = {
    "meeting_id": "f3a91c72-6d2e-4d3f-9c71-2f8c9e8b1a55",
    "meeting_title": "Retrieval Quality & Evaluation",
    "date": "2026-03-25",
    "participants": ["Ibrahim", "Sara", "Ali", "Hamza"],
    "transcript": [
        {"timestamp": "11:00:02", "speaker": "Ibrahim", "text": "Sync on retrieval quality: answers are inconsistent and we need better coverage."},
        {"timestamp": "11:00:27", "speaker": "Ibrahim", "text": "First: chunking. Our current chunks pull irrelevant context; we should reduce size and add overlap."},
        {"timestamp": "11:00:33", "speaker": "Hamza", "text": "Try ~300 chars with overlap; current too large leads to noisy retrieval."},
        {"timestamp": "11:01:07", "speaker": "Sara", "text": "Metadata: include speaker and timestamps so we can filter (e.g., 'what did Sara say')."},
        {"timestamp": "11:01:30", "speaker": "Ibrahim", "text": "We'll store speaker and other fields as metadata in the vector store; do not expose internal IDs in UI or LLM replies."},
        {"timestamp": "11:02:09", "speaker": "Ibrahim", "text": "Evaluation: create a small benchmark set of questions and expected answers to measure changes."},
        {"timestamp": "11:03:22", "speaker": "Ibrahim", "text": "Also force 'I don't know' when retrieval confidence is low; add a similarity threshold."},
        {"timestamp": "11:05:29", "speaker": "Ibrahim", "text": "Action: assemble a 20–30 example benchmark for decisions, action items and factual queries."}
    ]
}