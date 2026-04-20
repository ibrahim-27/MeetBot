def chunk_transcript(text: str, max_chars: int = 2800, overlap: int = 400) -> list[str]:
    """Split transcript into overlapping character windows (~700–900 tokens per chunk)."""
    text = (text or "").strip()
    if not text:
        return []
    if overlap >= max_chars:
        overlap = max(0, max_chars // 4)
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= n:
            break
        start += max_chars - overlap
    return chunks
