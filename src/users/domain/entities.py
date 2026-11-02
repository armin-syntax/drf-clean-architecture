from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class UserEntity:
    id: int
    public_id: UUID
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    followers_count: int = 0
    following_count: int = 0


@dataclass
class FollowEntity:
    follower_id: int
    following_id: int
