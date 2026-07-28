from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_dependencies import get_current_user
from app.api.dependencies import get_db
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationDetail, ConversationRead, ConversationUpdate
from app.services.conversations import create_conversation, delete_conversation, get_conversation, list_conversations, update_conversation

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.get("", response_model=list[ConversationRead])
async def read_conversations(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await list_conversations(db, user)

@router.post("", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
async def add_conversation(payload: ConversationCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_conversation(db, user, payload)

@router.get("/{conversation_id}", response_model=ConversationDetail)
async def read_conversation(conversation_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = await get_conversation(db, user, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.patch("/{conversation_id}", response_model=ConversationRead)
async def edit_conversation(conversation_id: int, payload: ConversationUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = await get_conversation(db, user, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return await update_conversation(db, conversation, payload)

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_conversation(conversation_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> Response:
    conversation = await get_conversation(db, user, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await delete_conversation(db, conversation)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
