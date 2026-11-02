from uuid import UUID

from posts.domain.entities import Post
from posts.domain.repositories import PostRepository


class CreatePost:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def execute(self, post: Post) -> Post:
        return self.repository.create(post)


class ListPosts:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def execute(self) -> list[Post]:
        return self.repository.list()


class GetPost:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def execute(self, public_id: UUID) -> Post:
        return self.repository.get_by_public_id(public_id)


class UpdatePost:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def execute(self, public_id: UUID, author_id: int, **kwargs) -> Post:
        return self.repository.update(public_id, author_id, **kwargs)


class DeletePost:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def execute(self, public_id: UUID, author_id: int) -> None:
        self.repository.delete(public_id, author_id)
