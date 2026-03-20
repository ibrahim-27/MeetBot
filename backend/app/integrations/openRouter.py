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
    
    async def summarize(self, transcript: dict) -> dict:
        prompt = f"""
        You are an expert project manager. Analyze the following meeting transcript and provide a structured summary.

        IMPORTANT:
        - Summary should be in bullet points in a list
        - If no clear action items are found, return an empty list: []. Do NOT invent placeholders.
        - If no clear key decisions are reached, return an empty list: [].
        - Use only the information provided in the transcript.

        Transcript:
        {transcript}

        Response Format:
        Strictly follow this JSON format:
        {{
            "summary": [
                "Summary point 1",
                "Summary point 2",
                "Summary point 3"
            ],
            "action_items": [
                "Task description (Assignee: Name, Deadline: Date/TBD)"
            ],
            "key_decisions": [
                "Decision reached"
            ]
        }}
        """

        messages = [
            {"role": "system", "content": "You are an expert project manager."},
            {"role": "user", "content": prompt}
        ]

        return await self.get_response(messages)