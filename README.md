# MeetBot

MeetBot ingests meeting transcripts, summarizes them, stores summaries in Notion, builds embeddings, and exposes a RAG-powered chat UI to ask questions about meetings.

## Quick overview
- Backend: FastAPI app (`backend/app`) — handles auth, chat, transcript processing, summarization, and embedding/storage.
- Frontend: Next.js app (`frontend`) — chat UI that talks to the backend APIs.
- Data: PostgreSQL (async SQLAlchemy) with `pgvector` for vector similarity.

## Requirements
- Python 3.11+ (backend)
- Node 18+ / npm (frontend)
- PostgreSQL with `pgvector` extension

## Required environment variables
- `DATABASE_URL` — async Postgres URL, e.g. `postgresql+asyncpg://user:pass@host:5432/dbname`
- `OPENROUTER_API_KEY` — API key for embeddings/LLM (or another LLM provider)
- `JWT_SECRET_KEY` — optional; a secret for JWT tokens (defaults exist for development)
- `NOTION_API_KEY` and `NOTION_DATABASE_ID` — optional, required only if you want Notion integration
- `EMBEDDING_MODEL`, `EMBEDDING_BATCH_SIZE`, `EMBEDDING_DIMENSIONS` — optional tuning vars

## Run backend (local)
1. Create and activate a virtualenv, install deps:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Create a `.env` with `DATABASE_URL` and `OPENROUTER_API_KEY` (and Notion keys if used).

3. Run the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Notes:
- On startup the app runs DB metadata creation and starts a scheduler that processes `backend/app/transcripts/*.py` fixtures to summarize and vectorize them.
- The scheduler uses the LLM for summarization and will attempt to write to Notion if Notion credentials are provided.

## Run frontend (local)
```bash
cd frontend
npm install
npm run dev
```

The UI expects the backend at `http://localhost:8000` by default.

## Where to look in the code
- Backend entry: `backend/app/main.py`
- Chat API and RAG logic: `backend/app/api/chat.py`
- LLM + embeddings wrapper: `backend/app/integrations/openRouter.py`
- Transcript processing job: `backend/app/jobs/transcript_job.py`
- DB models: `backend/app/models/*`
- Frontend chat UI and store: `frontend/components/chat`, `frontend/lib/store.ts`
