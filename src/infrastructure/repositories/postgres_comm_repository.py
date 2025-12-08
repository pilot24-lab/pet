from typing import List, Optional

from src.domain.entities.comment import Comment
from src.domain.repositories.comment_repository import CommentRepository
from src.infrastructure.database.connection import DatabaseConnection

class PostgresCommentRepository(CommentRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _map_row_to_comment(self, row) -> Optional[Comment]:
        if not row:
            return None
        return Comment(
            id=row['id'],
            user_id=row['user_id'],
            comment=row['comment'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    async def create(self, comment: Comment) -> Comment:
        row = await self.db.fetchrow(
            """
            insert into comments (user_id, comment)
            values ($1, $2)
            returning id, user_id, comment, created_at, updated_at
            """,
            comment.user_id, comment.comment
        )
        return self._map_row_to_comment(row)
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Comment]:
        rows = await self.db.fetch(
            """
            select id, user_id, comment, created_at, updated_at
            from comments
            order by id
            limit $1 offset $2
            """,
            limit, offset
        )
        return [self._map_row_to_comment(row) for row in rows]
    
    
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        row = await self.db.fetchrow(
            """
            select id, user_id, comment, created_at, updated_at
            from comments
            where id = $1
            """,
            comment_id
        )
        return self._map_row_to_comment(row)
    
    
    async def get_by_user_id(self, user_id: int, limit: int = 100, offset: int = 0) -> List[Comment]:
        rows = await self.db.fetch(
            """
            select id, user_id, comment, created_at, updated_at
            from comments
            where user_id = $1
            order by id
            limit $2 offset $3
        """, user_id, limit, offset
        )
        return [self._map_row_to_comment(row) for row in rows]
    
        
    async def update(self, comment: Comment) -> Optional[Comment]:
        row = await self.db.fetchrow(
            """
            update comments
            set comment = $1, updated_at = current_timestamp
            where id = $2
            returning  id, user_id, comment, created_at, updated_at
            """, comment.comment, comment.id
        )
        return self._map_row_to_comment(row)


    
    async def delete(self, comment_id: int) -> bool:
        result = await self.db.execute(
            """
            delete from comments
            where id = $1
            """,
            comment_id
        )
        return result == "DELETE 1"