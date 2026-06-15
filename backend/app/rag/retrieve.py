from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.openRouter import OpenRouter


async def retrieve_meeting_chunks(
    db: AsyncSession,
    query: str,
    *,
    limit: int = 8,
    max_context_chars: int = 12000,
) -> list[tuple[str, str, str, str]]:
    """Return (meeting_id, title, date, content) ranked by cosine distance to the query."""
    query = (query or "").strip()
    if not query:
        return []

    or_client = OpenRouter()
    embeddings = await or_client.embed([query])
    if not embeddings:
        return []
    vec = embeddings[0]
    vec_lit = "[" + ",".join(str(float(x)) for x in vec) + "]"

    stmt = text(
        """
        SELECT c.meeting_id, m.title, m.date, c.content
        FROM public.meeting_chunks c
        INNER JOIN public.meetings m ON m.id = c.meeting_id
        ORDER BY c.embedding <=> CAST(:qv AS vector)
        LIMIT :lim
        """
    )
    result = await db.execute(stmt, {"qv": vec_lit, "lim": limit})
    rows = result.fetchall()

    out: list[tuple[str, str, str, str]] = []
    total = 0
    for meeting_id, title, date, content in rows:
        if content is None:
            continue
        s = str(content).strip()
        if not s:
            continue
        meta = f"meeting_id={meeting_id}\ntitle={title or ''}\ndate={date or ''}\n"
        meta_len = len(meta)
        if total + meta_len + len(s) > max_context_chars:
            remaining = max_context_chars - total - meta_len
            if remaining <= 0:
                break
            s = s[:remaining]
        out.append((str(meeting_id), str(title or ""), str(date or ""), s))
        total += meta_len + len(s)
        if total >= max_context_chars:
            break
    return out
