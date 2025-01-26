import dataclasses as dc
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class PostStatusEnum(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

class CommentStatusEnum(Enum):
    HIDDEN = "hidden"
    PUBLIC = "public"

@dc.dataclass
class PostSchema:
    id: uuid.UUID
    title: str
    content: str
    status: PostStatusEnum
    date_created: datetime
    date_updated: Optional[datetime]
    
@dc.dataclass
class PostCreateSchema:
    title: Optional[str] = ""
    content: Optional[str] = ""
    status: Optional[PostStatusEnum] = PostStatusEnum.DRAFT


@dc.dataclass
class CommentSchema:
    id: uuid.UUID
    username: str
    content: str
    status: str
    date_created: datetime
    date_updated: datetime
    post_id: uuid

@dc.dataclass
class CommentCreateSchema:
    username: Optional[str] = ""
    content: Optional[str] = ""
    status: CommentStatusEnum = CommentStatusEnum.PUBLIC