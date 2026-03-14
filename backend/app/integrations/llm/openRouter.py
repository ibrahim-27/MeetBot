import httpx
import json
import os

class OpenRouter:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "<API_KEY_MISSING>")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def get_response(self, messages: list) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "openrouter/free",
            "messages": messages
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url=self.base_url,
                    headers=headers,
                    content=json.dumps(payload),
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']
            except Exception as e:
                return {"role": "assistant", "content": f"Error: {str(e)}"}