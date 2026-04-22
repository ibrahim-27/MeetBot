MEETING_5 = {
    "meeting_id": "f3a91c72-6d2e-4d3f-9c71-2f8c9e8b1a55",
    "meeting_title": "MeetBot Retrieval Quality & Evaluation Strategy",
    "date": "2026-03-25",
    "participants": [
        "Ibrahim",
        "Sara",
        "Ali",
        "Hamza"
    ],
    "transcript": [
        {
            "timestamp": "11:00:02",
            "speaker": "Ibrahim",
            "text": "Hey everyone, quick sync today on improving retrieval quality. Our current answers are okay but not consistent."
        },
        {
            "timestamp": "11:00:09",
            "speaker": "Sara",
            "text": "Yeah I noticed sometimes it misses obvious answers from the transcript."
        },
        {
            "timestamp": "11:00:14",
            "speaker": "Ali",
            "text": "Same here, especially when questions are slightly rephrased."
        },
        {
            "timestamp": "11:00:20",
            "speaker": "Hamza",
            "text": "That's likely embedding + chunking issues."
        },
        {
            "timestamp": "11:00:27",
            "speaker": "Ibrahim",
            "text": "Right. So first question: are we happy with current chunk size?"
        },
        {
            "timestamp": "11:00:33",
            "speaker": "Hamza",
            "text": "Right now it's 500 tokens with 50 overlap. I think it's too big."
        },
        {
            "timestamp": "11:00:40",
            "speaker": "Sara",
            "text": "Too big meaning?"
        },
        {
            "timestamp": "11:00:43",
            "speaker": "Hamza",
            "text": "Irrelevant info gets pulled in. Retrieval becomes noisy."
        },
        {
            "timestamp": "11:00:49",
            "speaker": "Ali",
            "text": "So reduce to maybe 300?"
        },
        {
            "timestamp": "11:00:52",
            "speaker": "Hamza",
            "text": "Yeah 300 with 75 overlap might be better."
        },
        {
            "timestamp": "11:00:58",
            "speaker": "Ibrahim",
            "text": "Ok let's try that. Second issue: metadata. We are not using speaker names or timestamps in retrieval."
        },
        {
            "timestamp": "11:01:07",
            "speaker": "Sara",
            "text": "Oh that could actually help a lot."
        },
        {
            "timestamp": "11:01:10",
            "speaker": "Ali",
            "text": "Like filtering by speaker?"
        },
        {
            "timestamp": "11:01:13",
            "speaker": "Ibrahim",
            "text": "Exactly. If someone asks what did Sara say, we should filter."
        },
        {
            "timestamp": "11:01:20",
            "speaker": "Hamza",
            "text": "We need to store metadata in vector DB then."
        },
        {
            "timestamp": "11:01:24",
            "speaker": "Ali",
            "text": "Chroma supports metadata filtering so that's doable."
        },
        {
            "timestamp": "11:01:30",
            "speaker": "Ibrahim",
            "text": "Great. Let's add speaker and meeting_id as metadata fields."
        },
        {
            "timestamp": "11:01:39",
            "speaker": "Sara",
            "text": "What about question rewriting before retrieval?"
        },
        {
            "timestamp": "11:01:43",
            "speaker": "Hamza",
            "text": "Yes! Query expansion or rewriting can improve recall."
        },
        {
            "timestamp": "11:01:49",
            "speaker": "Ali",
            "text": "But that adds latency right?"
        },
        {
            "timestamp": "11:01:53",
            "speaker": "Hamza",
            "text": "Slightly, but worth it for accuracy."
        },
        {
            "timestamp": "11:01:58",
            "speaker": "Ibrahim",
            "text": "Let's keep it optional behind a flag for now."
        },
        {
            "timestamp": "11:02:05",
            "speaker": "Sara",
            "text": "Good idea."
        },
        {
            "timestamp": "11:02:09",
            "speaker": "Ibrahim",
            "text": "Now evaluation. We don't really have a way to measure if changes improve things."
        },
        {
            "timestamp": "11:02:16",
            "speaker": "Ali",
            "text": "Yeah it's all manual testing right now."
        },
        {
            "timestamp": "11:02:20",
            "speaker": "Hamza",
            "text": "We should create a small benchmark dataset."
        },
        {
            "timestamp": "11:02:25",
            "speaker": "Sara",
            "text": "Like predefined questions and expected answers?"
        },
        {
            "timestamp": "11:02:29",
            "speaker": "Hamza",
            "text": "Exactly."
        },
        {
            "timestamp": "11:02:33",
            "speaker": "Ibrahim",
            "text": "How many examples to start?"
        },
        {
            "timestamp": "11:02:37",
            "speaker": "Hamza",
            "text": "Maybe 20 to 30 high quality ones."
        },
        {
            "timestamp": "11:02:42",
            "speaker": "Ali",
            "text": "We can cover different types: decisions, action items, general questions."
        },
        {
            "timestamp": "11:02:49",
            "speaker": "Sara",
            "text": "Also ambiguous queries to test robustness."
        },
        {
            "timestamp": "11:02:54",
            "speaker": "Ibrahim",
            "text": "Nice. And how do we score?"
        },
        {
            "timestamp": "11:03:00",
            "speaker": "Hamza",
            "text": "Could use LLM-as-judge or simple keyword matching initially."
        },
        {
            "timestamp": "11:03:07",
            "speaker": "Ali",
            "text": "LLM judge sounds more flexible."
        },
        {
            "timestamp": "11:03:11",
            "speaker": "Sara",
            "text": "But also more expensive."
        },
        {
            "timestamp": "11:03:15",
            "speaker": "Ibrahim",
            "text": "Let's start simple and upgrade later."
        },
        {
            "timestamp": "11:03:22",
            "speaker": "Ibrahim",
            "text": "Another issue: sometimes answers hallucinate when retrieval fails."
        },
        {
            "timestamp": "11:03:29",
            "speaker": "Ali",
            "text": "Yeah I've seen that."
        },
        {
            "timestamp": "11:03:32",
            "speaker": "Sara",
            "text": "We should force 'I don't know' behavior."
        },
        {
            "timestamp": "11:03:36",
            "speaker": "Hamza",
            "text": "We can add a threshold on similarity score."
        },
        {
            "timestamp": "11:03:41",
            "speaker": "Ibrahim",
            "text": "Below threshold, no answer."
        },
        {
            "timestamp": "11:03:45",
            "speaker": "Ali",
            "text": "And maybe show top retrieved chunks for debugging."
        },
        {
            "timestamp": "11:03:50",
            "speaker": "Sara",
            "text": "That would be super helpful for dev."
        },
        {
            "timestamp": "11:03:55",
            "speaker": "Ibrahim",
            "text": "Ok adding debug mode to UI."
        },
        {
            "timestamp": "11:04:02",
            "speaker": "Ibrahim",
            "text": "What about multi-meeting queries? Right now we only search one meeting."
        },
        {
            "timestamp": "11:04:09",
            "speaker": "Hamza",
            "text": "We should support global search across meetings."
        },
        {
            "timestamp": "11:04:13",
            "speaker": "Ali",
            "text": "That might mix contexts though."
        },
        {
            "timestamp": "11:04:17",
            "speaker": "Sara",
            "text": "Maybe default to current meeting, with option to expand."
        },
        {
            "timestamp": "11:04:22",
            "speaker": "Ibrahim",
            "text": "Yes, like a toggle: 'search all meetings'."
        },
        {
            "timestamp": "11:04:28",
            "speaker": "Hamza",
            "text": "We'll need meeting_id filtering for that."
        },
        {
            "timestamp": "11:04:32",
            "speaker": "Ali",
            "text": "Good thing we already planned metadata."
        },
        {
            "timestamp": "11:04:37",
            "speaker": "Ibrahim",
            "text": "Exactly."
        },
        {
            "timestamp": "11:04:42",
            "speaker": "Ibrahim",
            "text": "Last topic: caching responses."
        },
        {
            "timestamp": "11:04:46",
            "speaker": "Sara",
            "text": "For repeated queries?"
        },
        {
            "timestamp": "11:04:49",
            "speaker": "Ibrahim",
            "text": "Yes to reduce cost and latency."
        },
        {
            "timestamp": "11:04:53",
            "speaker": "Ali",
            "text": "We can hash queries."
        },
        {
            "timestamp": "11:04:56",
            "speaker": "Hamza",
            "text": "But careful with slight variations in wording."
        },
        {
            "timestamp": "11:05:01",
            "speaker": "Sara",
            "text": "Maybe cache after normalization."
        },
        {
            "timestamp": "11:05:05",
            "speaker": "Ibrahim",
            "text": "Good compromise."
        },
        {
            "timestamp": "11:05:10",
            "speaker": "Ibrahim",
            "text": "Alright let's assign actions."
        },
        {
            "timestamp": "11:05:14",
            "speaker": "Hamza",
            "text": "I'll update chunking strategy and add similarity threshold."
        },
        {
            "timestamp": "11:05:19",
            "speaker": "Ali",
            "text": "I'll implement metadata storage and filtering in Chroma."
        },
        {
            "timestamp": "11:05:24",
            "speaker": "Sara",
            "text": "I'll add debug mode UI and global search toggle."
        },
        {
            "timestamp": "11:05:29",
            "speaker": "Ibrahim",
            "text": "I'll create evaluation dataset and baseline scoring."
        },
        {
            "timestamp": "11:05:36",
            "speaker": "Sara",
            "text": "Timeline for this iteration?"
        },
        {
            "timestamp": "11:05:39",
            "speaker": "Ibrahim",
            "text": "Let's aim for 4 days and then re-evaluate."
        },
        {
            "timestamp": "11:05:44",
            "speaker": "Ali",
            "text": "Tight but doable."
        },
        {
            "timestamp": "11:05:48",
            "speaker": "Hamza",
            "text": "Yeah should be fine."
        },
        {
            "timestamp": "11:05:52",
            "speaker": "Sara",
            "text": "Cool let's do it."
        },
        {
            "timestamp": "11:05:56",
            "speaker": "Ibrahim",
            "text": "Great, thanks everyone. Let's see if we can actually move the needle on quality this time."
        }
    ]
}