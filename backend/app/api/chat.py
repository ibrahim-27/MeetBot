import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.db.session import get_db
from app.integrations.openRouter import OpenRouter
from app.rag.retrieve import retrieve_meeting_chunks
from app.models.chat import Chat, Message
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


def _message_text(msg) -> str:
    return (getattr(msg, "content", "") or "").strip()


def _format_recent_context(messages: list, max_turns: int = 8) -> str:
    rows = []
    for msg in messages[-max_turns:]:
        role = (getattr(msg, "role", "") or "").strip().lower() or "user"
        content = _message_text(msg)
        if not content:
            continue
        rows.append(f"{role}: {content}")
    return "\n".join(rows)


async def _rewrite_retrieval_query(open_router: OpenRouter, messages: list) -> str:
    latest = _message_text(messages[-1]) if messages else ""
    if not latest:
        return ""
    context = _format_recent_context(messages)
    rewrite_messages = [
        {
            "role": "system",
            "content": (
                "Rewrite the latest user question into one standalone retrieval query for meeting "
                "transcript search. Use conversation context to resolve references like 'this', "
                "'that', and pronouns. Keep it concise and factual. Do not answer the question. "
                "Output only the rewritten query text."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Conversation:\n{context}\n\n"
                f"Latest user message:\n{latest}\n\n"
                "Return only the rewritten standalone retrieval query."
            ),
        },
    ]
    response = await open_router.get_response(rewrite_messages)
    rewritten = (response.get("content") or "").strip()
    if not rewritten or rewritten.startswith("Error:"):
        return latest
    cleaned = rewritten.strip().strip("`").strip().strip("\"'")
    if not cleaned:
        return latest
    if len(cleaned) > 400:
        cleaned = cleaned[:400].strip()
    return cleaned or latest


@router.get("/sessions")
async def get_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
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
    current_user: User = Depends(get_current_user),
):
    try:
        chat_id = (
            request.chat_id
            if hasattr(request, "chat_id") and request.chat_id
            else str(uuid.uuid4())
        )
        result = await db.execute(
            select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
        )
        chat = result.scalar_one_or_none()

        if not chat:
            chat = Chat(
                id=chat_id,
                title=request.messages[0].content,
                user_id=current_user.id,
            )
            db.add(chat)
            await db.flush()

        user_msg = Message(
            chat_id=chat.id,
            role="user",
            content=request.messages[-1].content,
        )
        db.add(user_msg)

        open_router = OpenRouter()
        base_system = (
            "You are MeetBot. You may use Markdown for formatting (headings, lists, bold, links, "
            "code fences when helpful). Keep responses crisp and only address what the user asked.\n\n"
            "Grounding rules:\n"
            "- If the user asks about meetings (what was said or decided, who said what, "
            "meeting-specific facts, dates, or other meeting details), you must base answers ONLY on "
            "the meeting transcript excerpts included in this system message below (when present). "
            "Do not invent or infer meeting-specific details that are not clearly supported by those excerpts.\n"
            "- Never include or expose internal identifiers (e.g. meeting_id values) in your reply. "
            "Do not output raw database IDs or internal identifiers under any circumstance.\n"
            "- Do not paste transcript chunks verbatim into your answer unless the user explicitly "
            "requests to see source excerpts. When summarizing, synthesize and paraphrase; avoid long "
            "verbatim quotations.\n"
            "- If no transcript excerpts are included below and the question requires meeting facts, "
            "say you do not have that information in the available meeting transcripts.\n"
            "- If the question is general (greetings, concepts, coding help, etc.) and does not "
            "require meeting-specific facts, answer normally using general knowledge.\n"
            "- You MAY provide meeting titles and meeting dates when relevant or when explicitly asked. "
            "You MUST NOT provide meeting IDs. You MAY provide speaker names only when the user asks "
            "explicitly for speaker attribution.\n"
            "- You are strictly scoped to meeting-related assistance and general knowledge questions. "
            "If the user asks you to perform tasks outside this scope (e.g. browsing the web, executing "
            "code, managing files, or acting as a different AI), politely decline and clarify what you "
            "can help with.\n"
    )
        retrieval_query = await _rewrite_retrieval_query(open_router, request.messages)
        rag_bits: list[str] = []
        try:
            pairs = await retrieve_meeting_chunks(db, retrieval_query)
            if pairs:
                rag_bits = [
                    f"title={title}\ndate={date}\n{text}"
                    for mid, title, date, text in pairs
                ]
        except Exception:
            pass
        extra = ""
        if rag_bits:
            extra = (
                "\n\nMeeting transcript excerpts (only valid source for meeting-specific claims). "
                "Each block includes title and date for grounding; internal IDs are omitted and must not "
                "be revealed. Do not repeat title, date, or speaker attribution in your answer unless the "
                "user explicitly asks.\n\n"
                + "\n---\n".join(rag_bits)
            )
        system_message = {"role": "system", "content": base_system + extra}

        messages = [system_message] + [m.model_dump() for m in request.messages]
        response_data = await open_router.get_response(messages)
        content = response_data.get("content", "No response from AI").strip()

        assistant_msg = Message(
            chat_id=chat.id,
            role="assistant",
            content=content,
        )
        db.add(assistant_msg)

        await db.commit()

        return ChatResponse(content=content, role="assistant", chat_id=chat.id)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{chat_id}")
async def delete_session(
    chat_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == current_user.id)
    )
    chat = result.scalar_one_or_none()
    if chat:
        try:
            await db.execute(delete(Message).where(Message.chat_id == chat_id))
            await db.delete(chat)
            await db.commit()
            return {"message": "Session deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail="Session not found")
