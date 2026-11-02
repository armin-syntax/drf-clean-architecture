from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Post


class PostRepository(ABC):
    @abstractmethod
    def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    def list(self) -> list[Post]:
        pass

    @abstractmethod
    def get_by_public_id(self, public_id: UUID) -> Post:
        pass

    @abstractmethod
    def update(self, public_id: UUID, author_id: int, **kwargs) -> Post:
        pass

    @abstractmethod
    def delete(self, public_id: UUID, author_id: int) -> None:
        pass
