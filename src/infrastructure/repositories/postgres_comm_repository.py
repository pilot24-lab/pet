from typing import List, Optional

from src.domain.entities.comment import Comment
from src.domain.repositories.comment_repository import CommentRepository
from src.infrastructure.database.connection import DatabaseConnection

class PostgresCommentRepository(CommentRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _map_row_to_comment(self, row) -> Comment:
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
    