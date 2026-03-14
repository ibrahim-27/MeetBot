from app.integrations.llm.openRouter import OpenRouter
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.chat import Chat, Message
from app.schemas.chat import ChatRequest, ChatResponse
import uuid

router = APIRouter()

@router.get("/sessions")
async def get_sessions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chat).order_by(Chat.created_at.desc()))
    chats = result.scalars().all()
    return [{"id": chat.id, "title": chat.title} for chat in chats]

@router.post("/chat", response_model=ChatResponse)
async def get_response(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Get or Create Chat Session
        chat_id = request.chat_id if hasattr(request, 'chat_id') and request.chat_id else str(uuid.uuid4())
        result = await db.execute(select(Chat).where(Chat.id == chat_id))
        chat = result.scalar_one_or_none()
        
        if not chat:
            chat = Chat(id=chat_id, title="New Session")
            db.add(chat)
            await db.flush()

        # 2. Save User Message
        user_msg = Message(
            chat_id=chat.id,
            role="user",
            content=request.messages[-1].content
        )
        db.add(user_msg)

        # 3. Get AI Response
        openRouter = OpenRouter()
        system_message = {
            "role": "system",
            "content": "You are MeetBot. Always reply in plain text. Do not use Markdown. Emojis are allowed. Keep your responses as crisp and concise as possible."
        }
        
        # We should ideally fetch context from DB, but for now using the request messages
        messages = [system_message] + [m.model_dump() for m in request.messages]
        response_data = await openRouter.get_response(messages)
        content = response_data.get("content", "No response from AI")
        
        # 4. Save Assistant Message
        assistant_msg = Message(
            chat_id=chat.id,
            role="assistant",
            content=content
        )
        db.add(assistant_msg)
        
        await db.commit()
        
        return ChatResponse(
            content=content,
            role="assistant"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))