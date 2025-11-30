from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.comment_use_cases import (
    CreateCommentUseCase
)
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound, ValidationError
from src.presentation.api.dependencies import (
    get_create_comment_use_case
)
from src.presentation.schemas.comment_schemas import (
    CommentCreateRequest,
    CommentResponse
)

router = APIRouter(prefix='/comments', tags=['comments'])

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    request: CommentCreateRequest,
    use_case: CreateCommentUseCase = Depends(get_create_comment_use_case),
):
    try:
        comment_ex = await use_case.execute(user_id=request.user_id, comment=request.comment)
        return CommentResponse(
            id = comment_ex.id,
            user_id = comment_ex.user_id,
            comment = comment_ex.comment,
            created_at = comment_ex.created_at,
            updated_at = comment_ex.updated_at        
        )
    except EntityAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    


