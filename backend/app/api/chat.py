from app.integrations.llm.openRouter import OpenRouter
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def get_response(request: ChatRequest):
    try:
        openRouter = OpenRouter()
        
        # Define the system instruction
        system_message = {
            "role": "system",
            "content": "You are MeetBot. Always reply in plain text. Do not use Markdown (no **, no headers, etc.). Emojis are allowed. Keep your responses as crisp and concise as possible."
        }
        
        # Convert Pydantic models to list of dicts and prepend system message
        messages = [system_message] + [m.model_dump() for m in request.messages]
        response_data = await openRouter.get_response(messages)
        
        return ChatResponse(
            content=response_data.get("content", "No response from AI"),
            role=response_data.get("role", "assistant")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))