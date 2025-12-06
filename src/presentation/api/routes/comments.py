from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.comment_use_cases import (
    CreateCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentUseCase,
    GetAllCommentsUserIdUseCase
)
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound, ValidationError
from src.presentation.api.dependencies import (
    get_create_comment_use_case,
    get_get_all_comments_use_case,
    get_get_comment_use_case,
    get_get_all_comments_by_user_id_use_case
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
        comment = await use_case.execute(user_id=request.user_id, comment=request.comment)
        return CommentResponse(
            id = comment.id,
            user_id = comment.user_id,
            comment = comment.comment,
            created_at = comment.created_at,
            updated_at = comment.updated_at        
        )
    except EntityAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.get("/", response_model=List[CommentResponse])
async def get_all_comments(
    limit: int = 100,
    offset: int = 0,
    use_case: GetAllCommentsUseCase = Depends(get_get_all_comments_use_case)
):
    comments = await use_case.execute(limit=limit, offset=offset)
    return [
        CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            comment=comment.comment,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
        for comment in comments
    ]

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int, 
    use_case: GetCommentUseCase  = Depends(get_get_comment_use_case)
):
    try:
        comment = await use_case.execute(comment_id=comment_id)
        return CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            comment=comment.comment,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{comment_id}", response_model=List[CommentResponse])
async def get_comment_by_user_id(
    user_id: int, 
    use_case: GetAllCommentsUserIdUseCase  = Depends(get_get_all_comments_by_user_id_use_case)
):
    try:
        comments = await use_case.execute(user_id=user_id)
        return [
        CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            comment=comment.comment,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
        for comment in comments
    ]
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))