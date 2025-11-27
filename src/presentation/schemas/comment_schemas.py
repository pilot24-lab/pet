from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CommentCreateRequest(BaseModel):
    user_id: int
    comment: str