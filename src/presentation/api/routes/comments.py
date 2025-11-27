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
    CommentCreateRequest
)