from uuid import UUID

from posts.domain.entities import Post as PostEntity
from posts.domain.exceptions import PostNotFoundError
from posts.domain.repositories import PostRepository
from posts.infrastructure.models import Post as PostModel


def to_entity(post_model) -> PostEntity:
    return PostEntity(
        public_id=post_model.public_id,
        author_id=post_model.author_id,
        author_username=post_model.author.username,
        title=post_model.title,
        body=post_model.body,
        created_at=post_model.created_at,
        updated_at=post_model.updated_at,
    )


class DjangoPostRepository(PostRepository):
    def create(self, post: PostEntity) -> PostEntity:
        model = PostModel.objects.create(
            author_id=post.author_id,
            title=post.title,
            body=post.body,
        )
        model = PostModel.objects.select_related("author").get(pk=model.pk)
        return to_entity(model)

    def list(self) -> list[PostEntity]:
        posts = PostModel.objects.select_related("author").all()
        return [to_entity(item) for item in posts]

    def get_by_public_id(self, public_id: UUID) -> PostEntity:
        try:
            model = PostModel.objects.select_related("author").get(public_id=public_id)
            return to_entity(model)
        except PostModel.DoesNotExist:
            raise PostNotFoundError(f"Post with ID {public_id} not found.")

    def update(self, public_id: UUID, author_id: int, **kwargs) -> PostEntity:
        try:
            model = PostModel.objects.select_related("author").get(public_id=public_id, author_id=author_id)
        except PostModel.DoesNotExist:
            raise PostNotFoundError(f"Post not found or you don't have permission.")

        for key, value in kwargs.items():
            setattr(model, key, value)
        model.save()
        return to_entity(model)

    def delete(self, public_id: UUID, author_id: int) -> None:
        deleted_count, _ = PostModel.objects.filter(public_id=public_id, author_id=author_id).delete()
        
        if deleted_count == 0:
            raise PostNotFoundError(f"Post not found or you don't have permission.")
