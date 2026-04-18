import json
import os

import httpx


class OpenRouter:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "<API_KEY_MISSING>")
        base = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip().rstrip("/")
        self.base_url = f"{base}/chat/completions"

    async def get_response(self, messages: list) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": "openrouter/free", "messages": messages}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
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
