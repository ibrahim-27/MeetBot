import importlib.util
import json
from pathlib import Path

from sqlalchemy import delete

from app.db.session import AsyncSessionLocal
from app.integrations.notion import Notion
from app.integrations.openRouter import OpenRouter
from app.models.meeting import Meeting
from app.models.meeting_chunk import MeetingChunk
from app.rag.text_chunking import chunk_transcript


def load_meetings():
    folder = Path(__file__).resolve().parents[1] / "transcripts"
    out = []
    if not folder.exists():
        return out
    for path in sorted(folder.glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if not spec or not spec.loader:
            continue
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for v in vars(mod).values():
            if not isinstance(v, dict):
                continue
            if not all(k in v for k in ("meeting_id", "meeting_title", "transcript")):
                continue
            lines = []
            for row in v.get("transcript") or []:
                if isinstance(row, dict) and row.get("text", "").strip():
                    t = row["text"].strip()
                    ts, sp = str(row.get("timestamp", "")), str(row.get("speaker", ""))
                    lines.append(f"[{ts}] {sp}: {t}" if (ts or sp) else t)
            mid, title = str(v["meeting_id"]).strip(), str(v["meeting_title"]).strip()
            blob = "\n".join(lines)
            if mid and title and blob:
                out.append(
                    {
                        "meeting_id": mid,
                        "title": title,
                        "date": str(v.get("date", "")).strip(),
                        "transcript_text": blob,
                    }
                )
    return out


def parse_json_reply(text: str) -> dict:
    """Grab first {...} and json.loads; keys summary / action_items / key_decisions."""
    empty = {"summary": [], "action_items": [], "key_decisions": []}
    if not text or not text.strip():
        return empty
    i, j = text.find("{"), text.rfind("}")
    if i < 0 or j <= i:
        return empty
    try:
        d = json.loads(text[i : j + 1])
    except json.JSONDecodeError:
        return empty

    def lst(*keys):
        for k in keys:
            v = d.get(k)
            if v is None:
                continue
            if isinstance(v, list):
                out = [str(x).strip() for x in v if str(x).strip()]
                if out:
                    return out
            elif str(v).strip():
                return [str(v).strip()]
        return []

    return {
        "summary": lst("summary", "Summary"),
        "action_items": lst("action_items", "actionItems", "Action Items"),
        "key_decisions": lst("key_decisions", "keyDecisions", "Key Decisions", "decisions"),
    }


def good_enough(parsed: dict, raw: str) -> bool:
    if not raw or not raw.strip():
        return False
    if raw.strip().startswith("Error:"):
        return False
    return bool(parsed.get("summary"))


async def run_transcript_summary_job():
    items = load_meetings()
    if not items:
        return {
            "loaded": 0,
            "summarized": 0,
            "skipped": 0,
            "failed": 0,
            "vectorized": 0,
            "failed_embed": 0,
        }

    llm = OpenRouter()
    notion = Notion()
    summarized = skipped = failed = 0
    vectorized = failed_embed = 0

    for rec in items:
        async with AsyncSessionLocal() as db:
            row = await db.get(Meeting, rec["meeting_id"])
            if row is None:
                db.add(
                    Meeting(
                        id=rec["meeting_id"],
                        title=rec["title"],
                        date=rec["date"],
                        is_summarised=False,
                        is_vectorized=False,
                    )
                )
            else:
                row.title = rec["title"]
                row.date = rec["date"]
            await db.commit()

        async with AsyncSessionLocal() as db:
            row = await db.get(Meeting, rec["meeting_id"])
            if row is None:
                continue
            if row.is_summarised and row.is_vectorized:
                skipped += 1
                continue
            need_summary = not row.is_summarised

        if need_summary:
            msg = await llm.summarize(
                {
                    "meeting_id": rec["meeting_id"],
                    "meeting_title": rec["title"],
                    "date": rec["date"],
                    "transcript_text": rec["transcript_text"],
                }
            )
            raw = (msg.get("content") or "").strip()
            print(f"[LLM] meeting_id={rec['meeting_id']!r}\n{raw}\n---")
            parsed = parse_json_reply(raw)
            print(f"[parsed] {parsed}")

            if not good_enough(parsed, raw):
                failed += 1
            else:
                await notion.create_page(rec["meeting_id"], rec["title"], rec["date"], parsed)
                async with AsyncSessionLocal() as db:
                    row = await db.get(Meeting, rec["meeting_id"])
                    if row:
                        row.is_summarised = True
                        await db.commit()
                summarized += 1

        mid = rec["meeting_id"]
        chunks = chunk_transcript(rec["transcript_text"])

        async with AsyncSessionLocal() as db:
            row = await db.get(Meeting, mid)
            if row is None or row.is_vectorized:
                continue

            if not chunks:
                row.is_vectorized = True
                await db.commit()
                vectorized += 1
                continue

        try:
            embeddings = await llm.embed(chunks)
        except Exception as e:
            print(f"[embed] meeting_id={mid!r} failed: {e}")
            failed_embed += 1
            continue

        async with AsyncSessionLocal() as db:
            row = await db.get(Meeting, mid)
            if row is None or row.is_vectorized:
                continue

            await db.execute(delete(MeetingChunk).where(MeetingChunk.meeting_id == mid))
            for idx, (piece, vec) in enumerate(zip(chunks, embeddings)):
                db.add(
                    MeetingChunk(
                        meeting_id=mid,
                        chunk_index=idx,
                        content=piece,
                        embedding=vec,
                    )
                )
            row.is_vectorized = True
            await db.commit()
            vectorized += 1

    return {
        "loaded": len(items),
        "summarized": summarized,
        "skipped": skipped,
        "failed": failed,
        "vectorized": vectorized,
        "failed_embed": failed_embed,
    }
