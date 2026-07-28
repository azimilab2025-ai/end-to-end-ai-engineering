from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=20000)

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
