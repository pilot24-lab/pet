from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int, limit: int = 100, offset: int = 0) -> List[Comment]:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Comment]:
        pass

    @abstractmethod
    async def update(self, comment: Comment) -> Optional[Comment]:
        pass
    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        pass
