MEETING_1 = {
    "meeting_id": "ac67465e-810f-4186-877f-15744514525a",
    "meeting_title": "MeetBot Brainstorming",
    "date": "2026-03-18",
    "participants": [
        "Ibrahim",
        "Sara",
        "Ali",
        "Hamza"
    ],
    "transcript": [
        {
            "timestamp": "10:00:03",
            "speaker": "Ibrahim",
            "text": "Hey everyone, can you hear me?"
        },
        {
            "timestamp": "10:00:06",
            "speaker": "Sara",
            "text": "Yes, loud and clear."
        },
        {
            "timestamp": "10:00:08",
            "speaker": "Ali",
            "text": "Yeah I can hear you."
        },
        {
            "timestamp": "10:00:10",
            "speaker": "Hamza",
            "text": "Same here."
        },
        {
            "timestamp": "10:00:15",
            "speaker": "Ibrahim",
            "text": "Great. Thanks for joining. So today I wanted to brainstorm this MeetBot idea I've been thinking about. Basically it's an AI meeting assistant that can take meeting transcripts, summarize them, store them in Notion, and then allow users to ask questions later through a conversational agent."
        },
        {
            "timestamp": "10:00:37",
            "speaker": "Sara",
            "text": "So kind of like Otter.ai but more focused on knowledge retrieval?"
        },
        {
            "timestamp": "10:00:42",
            "speaker": "Ibrahim",
            "text": "Exactly. Less about transcription and more about building a knowledge base from meetings."
        },
        {
            "timestamp": "10:00:51",
            "speaker": "Ali",
            "text": "Are we planning to integrate with Zoom or something?"
        },
        {
            "timestamp": "10:00:55",
            "speaker": "Ibrahim",
            "text": "Not initially. I think that might slow us down. We can just start with transcript files."
        },
        {
            "timestamp": "10:01:04",
            "speaker": "Hamza",
            "text": "Yeah honestly meeting provider APIs can become a project on their own."
        },
        {
            "timestamp": "10:01:10",
            "speaker": "Sara",
            "text": "Yeah makes sense for MVP."
        },
        {
            "timestamp": "10:01:18",
            "speaker": "Ibrahim",
            "text": "The main flow I am thinking is transcript comes in, we process it, generate summary, store in Notion, then create embeddings and allow a RAG based chat."
        },
        {
            "timestamp": "10:01:35",
            "speaker": "Hamza",
            "text": "We should definitely do chunking properly otherwise retrieval will be bad."
        },
        {
            "timestamp": "10:01:41",
            "speaker": "Ali",
            "text": "Yeah and maybe add overlap between chunks."
        },
        {
            "timestamp": "10:01:47",
            "speaker": "Ibrahim",
            "text": "Agreed."
        },
        {
            "timestamp": "10:01:52",
            "speaker": "Sara",
            "text": "What about frontend stack?"
        },
        {
            "timestamp": "10:01:56",
            "speaker": "Ibrahim",
            "text": "Yeah let's decide that."
        },
        {
            "timestamp": "10:02:02",
            "speaker": "Sara",
            "text": "I mean React is the obvious choice."
        },
        {
            "timestamp": "10:02:06",
            "speaker": "Ali",
            "text": "Yeah standard choice."
        },
        {
            "timestamp": "10:02:10",
            "speaker": "Hamza",
            "text": "What about Next.js instead of plain React?"
        },
        {
            "timestamp": "10:02:14",
            "speaker": "Sara",
            "text": "Why Next specifically?"
        },
        {
            "timestamp": "10:02:19",
            "speaker": "Hamza",
            "text": "Built-in routing, server components, API routes if needed."
        },
        {
            "timestamp": "10:02:28",
            "speaker": "Ali",
            "text": "Also deployment becomes easier with Vercel."
        },
        {
            "timestamp": "10:02:34",
            "speaker": "Ibrahim",
            "text": "True. And we might need some backend functionality anyway."
        },
        {
            "timestamp": "10:02:40",
            "speaker": "Sara",
            "text": "Yeah that actually makes sense."
        },
        {
            "timestamp": "10:02:47",
            "speaker": "Ibrahim",
            "text": "Any downside?"
        },
        {
            "timestamp": "10:02:51",
            "speaker": "Sara",
            "text": "Not really. Slight learning curve but worth it."
        },
        {
            "timestamp": "10:02:59",
            "speaker": "Ali",
            "text": "I think Next.js is better long term."
        },
        {
            "timestamp": "10:03:05",
            "speaker": "Ibrahim",
            "text": "Ok sounds good. Let's go with Next.js then."
        },
        {
            "timestamp": "10:03:12",
            "speaker": "Sara",
            "text": "Works for me."
        },
        {
            "timestamp": "10:03:15",
            "speaker": "Hamza",
            "text": "Same."
        },
        {
            "timestamp": "10:03:19",
            "speaker": "Ali",
            "text": "Yep."
        },
        {
            "timestamp": "10:03:28",
            "speaker": "Ibrahim",
            "text": "Backend options?"
        },
        {
            "timestamp": "10:03:32",
            "speaker": "Ali",
            "text": "Node.js would be easiest since we all know it."
        },
        {
            "timestamp": "10:03:39",
            "speaker": "Sara",
            "text": "Express maybe?"
        },
        {
            "timestamp": "10:03:43",
            "speaker": "Hamza",
            "text": "For AI work Python might be easier though."
        },
        {
            "timestamp": "10:03:49",
            "speaker": "Ibrahim",
            "text": "True. Most RAG tooling is Python."
        },
        {
            "timestamp": "10:03:55",
            "speaker": "Hamza",
            "text": "LangChain, LlamaIndex, all Python first."
        },
        {
            "timestamp": "10:04:03",
            "speaker": "Ali",
            "text": "That is true."
        },
        {
            "timestamp": "10:04:09",
            "speaker": "Ibrahim",
            "text": "What about FastAPI?"
        },
        {
            "timestamp": "10:04:14",
            "speaker": "Hamza",
            "text": "Yeah FastAPI is great. Async, fast, automatic docs."
        },
        {
            "timestamp": "10:04:22",
            "speaker": "Sara",
            "text": "Does it integrate easily with AI libraries?"
        },
        {
            "timestamp": "10:04:26",
            "speaker": "Hamza",
            "text": "Very easily."
        },
        {
            "timestamp": "10:04:30",
            "speaker": "Ali",
            "text": "Swagger docs automatically is nice too."
        },
        {
            "timestamp": "10:04:36",
            "speaker": "Ibrahim",
            "text": "Ok I am leaning FastAPI then."
        },
        {
            "timestamp": "10:04:41",
            "speaker": "Sara",
            "text": "Sounds good."
        },
        {
            "timestamp": "10:04:45",
            "speaker": "Ali",
            "text": "Yeah let's do that."
        },
        {
            "timestamp": "10:04:52",
            "speaker": "Ibrahim",
            "text": "Ok backend FastAPI."
        },
        {
            "timestamp": "10:05:02",
            "speaker": "Ibrahim",
            "text": "Now LLM provider."
        },
        {
            "timestamp": "10:05:06",
            "speaker": "Hamza",
            "text": "OpenAI is easiest."
        },
        {
            "timestamp": "10:05:10",
            "speaker": "Ali",
            "text": "Yeah GPT APIs are clean."
        },
        {
            "timestamp": "10:05:16",
            "speaker": "Sara",
            "text": "Cost might become issue though."
        },
        {
            "timestamp": "10:05:22",
            "speaker": "Ibrahim",
            "text": "Yeah since this is personal project maybe we reduce cost."
        },
        {
            "timestamp": "10:05:30",
            "speaker": "Hamza",
            "text": "We could use OpenRouter."
        },
        {
            "timestamp": "10:05:35",
            "speaker": "Ali",
            "text": "Oh yeah that gives multiple models."
        },
        {
            "timestamp": "10:05:39",
            "speaker": "Hamza",
            "text": "And some free models too."
        },
        {
            "timestamp": "10:05:45",
            "speaker": "Ibrahim",
            "text": "API similar to OpenAI?"
        },
        {
            "timestamp": "10:05:49",
            "speaker": "Hamza",
            "text": "Yes same format."
        },
        {
            "timestamp": "10:05:53",
            "speaker": "Sara",
            "text": "Then switching later should be easy."
        },
        {
            "timestamp": "10:05:58",
            "speaker": "Ibrahim",
            "text": "Ok let's start with OpenRouter."
        },
        {
            "timestamp": "10:06:05",
            "speaker": "Ali",
            "text": "Makes sense."
        },
        {
            "timestamp": "10:06:14",
            "speaker": "Ibrahim",
            "text": "Vector database?"
        },
        {
            "timestamp": "10:06:18",
            "speaker": "Hamza",
            "text": "Chroma easiest locally."
        },
        {
            "timestamp": "10:06:22",
            "speaker": "Ali",
            "text": "Pinecone if cloud later."
        },
        {
            "timestamp": "10:06:27",
            "speaker": "Sara",
            "text": "Let's keep simple first."
        },
        {
            "timestamp": "10:06:31",
            "speaker": "Ibrahim",
            "text": "Ok Chroma for MVP."
        },
        {
            "timestamp": "10:06:40",
            "speaker": "Ibrahim",
            "text": "Notion integration. What should we store?"
        },
        {
            "timestamp": "10:06:46",
            "speaker": "Sara",
            "text": "Summary definitely."
        },
        {
            "timestamp": "10:06:50",
            "speaker": "Ali",
            "text": "Transcript maybe."
        },
        {
            "timestamp": "10:06:54",
            "speaker": "Hamza",
            "text": "Action items."
        },
        {
            "timestamp": "10:06:58",
            "speaker": "Ibrahim",
            "text": "Maybe decisions too."
        },
        {
            "timestamp": "10:07:03",
            "speaker": "Sara",
            "text": "Good idea."
        },
        {
            "timestamp": "10:07:08",
            "speaker": "Ibrahim",
            "text": "So fields: meeting title, date, summary, transcript, action items."
        },
        {
            "timestamp": "10:07:18",
            "speaker": "Ali",
            "text": "Maybe tags too later."
        },
        {
            "timestamp": "10:07:23",
            "speaker": "Ibrahim",
            "text": "Yeah phase two."
        },
        {
            "timestamp": "10:07:32",
            "speaker": "Ibrahim",
            "text": "Conversational agent features?"
        },
        {
            "timestamp": "10:07:36",
            "speaker": "Sara",
            "text": "Greeting message."
        },
        {
            "timestamp": "10:07:40",
            "speaker": "Hamza",
            "text": "Context aware answers."
        },
        {
            "timestamp": "10:07:44",
            "speaker": "Ali",
            "text": "Ask about decisions."
        },
        {
            "timestamp": "10:07:49",
            "speaker": "Ibrahim",
            "text": "Example question could be what backend did we choose."
        },
        {
            "timestamp": "10:07:57",
            "speaker": "Hamza",
            "text": "Agent should answer FastAPI and why."
        },
        {
            "timestamp": "10:08:04",
            "speaker": "Sara",
            "text": "Also action items per person."
        },
        {
            "timestamp": "10:08:09",
            "speaker": "Ali",
            "text": "Yeah like what tasks do I have."
        },
        {
            "timestamp": "10:08:15",
            "speaker": "Ibrahim",
            "text": "Good."
        },
        {
            "timestamp": "10:08:26",
            "speaker": "Ibrahim",
            "text": "Future features?"
        },
        {
            "timestamp": "10:08:30",
            "speaker": "Sara",
            "text": "Dashboard."
        },
        {
            "timestamp": "10:08:34",
            "speaker": "Ali",
            "text": "Search across meetings."
        },
        {
            "timestamp": "10:08:38",
            "speaker": "Hamza",
            "text": "Auto action item extraction."
        },
        {
            "timestamp": "10:08:45",
            "speaker": "Ibrahim",
            "text": "Maybe Slack integration later."
        },
        {
            "timestamp": "10:08:54",
            "speaker": "Ibrahim",
            "text": "Ok let's assign tasks."
        },
        {
            "timestamp": "10:09:00",
            "speaker": "Sara",
            "text": "I can handle frontend."
        },
        {
            "timestamp": "10:09:04",
            "speaker": "Ali",
            "text": "I'll take backend APIs."
        },
        {
            "timestamp": "10:09:08",
            "speaker": "Hamza",
            "text": "I'll work on RAG pipeline."
        },
        {
            "timestamp": "10:09:13",
            "speaker": "Ibrahim",
            "text": "I'll do Notion integration and orchestration."
        },
        {
            "timestamp": "10:09:22",
            "speaker": "Sara",
            "text": "Timeline?"
        },
        {
            "timestamp": "10:09:26",
            "speaker": "Ibrahim",
            "text": "Maybe 2 to 3 weeks MVP."
        },
        {
            "timestamp": "10:09:31",
            "speaker": "Ali",
            "text": "Reasonable."
        },
        {
            "timestamp": "10:09:36",
            "speaker": "Hamza",
            "text": "Yeah doable."
        },
        {
            "timestamp": "10:09:42",
            "speaker": "Ibrahim",
            "text": "Alright sounds like a plan."
        },
        {
            "timestamp": "10:09:48",
            "speaker": "Sara",
            "text": "Looking forward to it."
        },
        {
            "timestamp": "10:09:52",
            "speaker": "Ali",
            "text": "Same here."
        },
        {
            "timestamp": "10:09:56",
            "speaker": "Hamza",
            "text": "Should be fun."
        },
        {
            "timestamp": "10:10:02",
            "speaker": "Ibrahim",
            "text": "Thanks everyone. Let's sync next week."
        },
        {
            "timestamp": "10:10:07",
            "speaker": "Sara",
            "text": "Bye."
        },
        {
            "timestamp": "10:10:09",
            "speaker": "Ali",
            "text": "Bye."
        },
        {
            "timestamp": "10:10:11",
            "speaker": "Hamza",
            "text": "Bye."
        }
    ]
}