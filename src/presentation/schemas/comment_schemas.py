from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CommentCreateRequest(BaseModel):
    user_id: int
    comment: str

class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    comment: str
    created_at: datetime
    updated_at: datetime

class CommentUpdateRequest(BaseModel):
    comment: Optional[str] = None
    user_id: int