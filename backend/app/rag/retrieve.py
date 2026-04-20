from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.openRouter import OpenRouter


async def retrieve_meeting_chunks(
    db: AsyncSession,
    query: str,
    *,
    limit: int = 8,
    max_context_chars: int = 12000,
) -> list[tuple[str, str]]:
    """Return (meeting_id, content) rows ranked by cosine distance to the query embedding."""
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
        SELECT meeting_id, content
        FROM public.meeting_chunks
        ORDER BY embedding <=> CAST(:qv AS vector)
        LIMIT :lim
        """
    )
    result = await db.execute(stmt, {"qv": vec_lit, "lim": limit})
    rows = result.fetchall()

    out: list[tuple[str, str]] = []
    total = 0
    for meeting_id, content in rows:
        if content is None:
            continue
        s = str(content).strip()
        if not s:
            continue
        if total + len(s) > max_context_chars:
            remaining = max_context_chars - total
            if remaining <= 0:
                break
            s = s[:remaining]
        out.append((str(meeting_id), s))
        total += len(s)
        if total >= max_context_chars:
            break
    return out
