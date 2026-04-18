from typing import List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    chat_id: Optional[str] = None


class ChatResponse(BaseModel):
    content: str
    role: str = "assistant"
    chat_id: Optional[str] = None
