from app.integrations.llm.openRouter import OpenRouter
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.chat import Chat, Message, User
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.auth import get_current_user
import uuid

router = APIRouter()

@router.get("/sessions")
async def get_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    )
    chats = result.scalars().all()
    return [{"id": chat.id, "title": chat.title} for chat in chats]

@router.get("/sessions/{chat_id}/messages")
async def get_messages(
    chat_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify chat ownership
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    return [{"role": msg.role, "content": msg.content} for msg in messages]

@router.post("/chat", response_model=ChatResponse)
async def get_response(
    request: ChatRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # 1. Get or Create Chat Session
        chat_id = request.chat_id if hasattr(request, 'chat_id') and request.chat_id else str(uuid.uuid4())
        result = await db.execute(
            select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
        )
        chat = result.scalar_one_or_none()
        
        if not chat:
            # If it's a new ID, create it for current user
            chat = Chat(id=chat_id, title=request.messages[0].content, user_id=current_user.id)
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
        
        # Using request messages + context
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
            role="assistant",
            chat_id=chat.id
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{chat_id}")
async def delete_session(
    chat_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    if chat:
        try:
            from sqlalchemy import delete
            await db.execute(delete(Message).where(Message.chat_id == chat_id))
            await db.delete(chat)
            await db.commit()
            return {"message": "Session deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Session not found")