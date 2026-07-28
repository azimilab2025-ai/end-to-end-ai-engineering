from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationUpdate

async def list_conversations(db: AsyncSession, user: User) -> list[Conversation]:
    result = await db.execute(select(Conversation).where(Conversation.user_id == user.id).order_by(Conversation.updated_at.desc()))
    return list(result.scalars().all())

async def get_conversation(db: AsyncSession, user: User, conversation_id: int) -> Conversation | None:
    result = await db.execute(select(Conversation).options(selectinload(Conversation.messages)).where(Conversation.id == conversation_id, Conversation.user_id == user.id))
    return result.scalar_one_or_none()

async def create_conversation(db: AsyncSession, user: User, payload: ConversationCreate) -> Conversation:
    conversation = Conversation(user_id=user.id, title=payload.title)
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation

async def update_conversation(db: AsyncSession, conversation: Conversation, payload: ConversationUpdate) -> Conversation:
    conversation.title = payload.title
    await db.commit()
    await db.refresh(conversation)
    return conversation

async def delete_conversation(db: AsyncSession, conversation: Conversation) -> None:
    await db.delete(conversation)
    await db.commit()
