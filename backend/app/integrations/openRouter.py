import json
import os

import httpx


class OpenRouter:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "<API_KEY_MISSING>")
        base = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip().rstrip("/")
        self.chat_url = f"{base}/chat/completions"
        self.embeddings_url = f"{base}/embeddings"
        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL",
            "openai/text-embedding-3-small",
        ).strip()
        self.embed_batch_size = int(os.getenv("EMBEDDING_BATCH_SIZE", "64"))

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts using OpenRouter embeddings API (batched)."""
        if not texts:
            return []
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        out: list[list[float]] = []
        batch = max(1, self.embed_batch_size)

        async with httpx.AsyncClient() as client:
            for i in range(0, len(texts), batch):
                chunk = texts[i : i + batch]
                payload = {"model": self.embedding_model, "input": chunk}
                try:
                    response = await client.post(
                        self.embeddings_url,
                        headers=headers,
                        json=payload,
                        timeout=120.0,
                    )
                    response.raise_for_status()
                    data = response.json().get("data") or []
                    data.sort(key=lambda d: d.get("index", 0))
                    for row in data:
                        emb = row.get("embedding")
                        if emb is None:
                            raise ValueError("Missing embedding in API response")
                        out.append(list(map(float, emb)))
                except Exception as e:
                    raise RuntimeError(f"Embeddings request failed: {e!s}") from e

        if len(out) != len(texts):
            raise ValueError(f"Embedding count mismatch: expected {len(texts)}, got {len(out)}")
        return out

    async def get_response(self, messages: list) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": "openrouter/free", "messages": messages}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.chat_url,
                    headers=headers,
                    json=payload,
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]
            except Exception as e:
                return {"role": "assistant", "content": f"Error: {e!s}"}

    async def summarize(self, transcript: dict) -> dict:
        user = (
            "Return JSON only with keys summary, action_items, key_decisions "
            "(each a list of strings).\n"
            f"{json.dumps(transcript, ensure_ascii=False)}"
        )
        messages = [
            {"role": "system", "content": "You summarize meetings."},
            {"role": "user", "content": user},
        ]
        return await self.get_response(messages)
