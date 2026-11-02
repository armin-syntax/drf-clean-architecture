from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Post:
    public_id: Optional[UUID]
    author_id: int
    author_username: Optional[str]
    title: str
    body: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
