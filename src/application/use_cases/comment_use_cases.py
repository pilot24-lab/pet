from typing import List, Optional

from src.domain.entities.comment import Comment
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound, ValidationError
from src.domain.repositories.comment_repository import CommentRepository
from src.application.use_cases.user_use_cases import GetUserUseCase

class CreateCommentUseCase:
    def __init__(self, commetn_repository: CommentRepository):
        self.comment_repository = commetn_repository

    async def execute(self, user_id: int, comment: str) -> Comment:
        if not comment or not user_id:
            raise ValidationError('User_id and Comment are required')
        existing_user = GetUserUseCase.execute(user_id)
        if not existing_user:
            raise EntityNotFound(f"User with id {user_id} not found")
        comment = Comment(id=None, user_id=user_id, comment=comment)
        return await self.comment_repository.create(comment)
       

class GetCommentUseCase:
    def __init__(self, commetn_repository: CommentRepository):
        self.comment_repository = commetn_repository

    async def execute(self, comment_id: int) -> Comment:
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise EntityNotFound(f"Comment with id {comment_id} not found")
        return comment        


class GetAllCommentsUserIdUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
    
    async def execute(self, user_id: int, limit: int = 100, offset: int = 0) -> List[Comment]:
        existing_user = GetUserUseCase.execute(user_id)
        if not existing_user:
            raise EntityNotFound(f"User with id {user_id} not found")
        return await self.comment_repository.get_by_user_id(user_id=user_id, limit=limit, offset=offset)
        

class GetAllCommentsUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(self, limit: int = 100, offset: int = 0) -> List[Comment]:
        return await self.comment_repository.get_all(limit=limit, offset=offset)

class UpdateCommentUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        
    async def execute(self, comment: str, user_id: int, comment_id: int) -> Comment:
        existing_comment = await self.comment_repository.get_by_id(comment_id)
        
        if not existing_comment:
            raise EntityNotFound(f"Comment with {comment_id} user_id is not found")
        if comment:
            existing_comment.comment = comment
        return await self.comment_repository.update(existing_comment)
             

class DeleteCommentUseCase:
    def __init__(self, comment_repositoty: CommentRepository):
        self.comment_repository = comment_repositoty

    async def execute(self, comment_id: int) -> bool:
        result = await self.comment_repository.delete(comment_id)
        if not result:
            raise EntityNotFound(f"Comment with {comment_id} is not found")
        return result

        