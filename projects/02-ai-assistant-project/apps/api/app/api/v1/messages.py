from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_dependencies import get_current_user
from app.api.dependencies import get_db
from app.models.user import User
from app.schemas.message import MessageCreate, MessageRead
from app.services.assistant import generate_assistant_reply
from app.services.conversations import get_conversation
from app.services.messages import create_message, message_history

router = APIRouter(prefix="/conversations", tags=["Assistant"])

@router.post("/{conversation_id}/messages", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def send_message(conversation_id: int, payload: MessageCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = await get_conversation(db, user, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await create_message(db, conversation_id, "user", payload.content)
    history = await message_history(db, conversation_id)
    reply = await generate_assistant_reply([{"role": item.role, "content": item.content} for item in history])
    return await create_message(db, conversation_id, "assistant", reply)
