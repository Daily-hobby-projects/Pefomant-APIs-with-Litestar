import dataclasses as dc
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class StatusEnum(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

@dc.dataclass
class PostSchema:
    uid: uuid.UUID
    title: str
    content: str
    status: StatusEnum
    date_created: datetime
    date_updated: Optional[datetime]
    
@dc.dataclass
class PostCreateSchema:
    title: str
    content: str
    status: Optional[StatusEnum] = StatusEnum.DRAFT
