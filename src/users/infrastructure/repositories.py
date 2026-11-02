from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import connections

from users.domain.entities import UserEntity
from users.domain.exceptions import UserNotFoundError
from users.domain.repositories import UserRepository, ExternalUserRepository
from users.infrastructure.models import Follow

UserModel = get_user_model()


def to_entity(user) -> UserEntity:
    return UserEntity(
        id=user.id,
        public_id=user.public_id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        avatar=user.avatar.url if user.avatar else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
        followers_count=user.follower_relations.count(),
        following_count=user.following_relations.count(),
    )


class DjangoUserRepository(UserRepository):
    def get_by_username(self, username: str) -> UserEntity:
        try:
            return to_entity(UserModel.objects.get(username=username))
        except UserModel.DoesNotExist:
            raise UserNotFoundError(f"User with username '{username}' not found.")

    def list(self) -> list[UserEntity]:
        return [to_entity(user) for user in UserModel.objects.all()]

    def create(self, username: str, email: str, password: str, **kwargs) -> UserEntity:
        user = UserModel.objects.create_user(username=username, email=email, password=password, **kwargs)
        return to_entity(user)

    def update(self, username: str, **kwargs) -> UserEntity:
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise UserNotFoundError(f"User with username '{username}' not found.")
            
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return to_entity(user)

    def delete(self, username: str) -> None:
        try:
            user = UserModel.objects.get(username=username)
            user.delete()
        except UserModel.DoesNotExist:
            raise UserNotFoundError(f"User with username '{username}' not found.")

    def follow(self, follower_username: str, following_username: str) -> None:
        if follower_username.lower() == following_username.lower():
            raise ValueError("You cannot follow yourself.")
        
        try:
            follower = UserModel.objects.get(username=follower_username)
            following = UserModel.objects.get(username=following_username)
        except UserModel.DoesNotExist:
            raise UserNotFoundError("One of the users was not found.")
            
        Follow.objects.get_or_create(follower=follower, following=following)

    def unfollow(self, follower_username: str, following_username: str) -> None:
        if follower_username.lower() == following_username.lower():
            raise ValueError("You cannot unfollow yourself.")
            
        try:
            follower = UserModel.objects.get(username=follower_username)
            following = UserModel.objects.get(username=following_username)
        except UserModel.DoesNotExist:
            raise UserNotFoundError("One of the users was not found.")
            
        Follow.objects.filter(follower=follower, following=following).delete()

    def get_followers(self, username: str) -> list[UserEntity]:
        users = UserModel.objects.filter(following_relations__following__username=username).distinct()
        return [to_entity(user) for user in users]

    def get_following(self, username: str) -> list[UserEntity]:
        users = UserModel.objects.filter(follower_relations__follower__username=username).distinct()
        return [to_entity(user) for user in users]

    def check_username_exists(self, username: str) -> bool:
        return UserModel.objects.filter(username=username).exists()

    def check_email_exists(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()


class SqliteExternalUserRepository(ExternalUserRepository):
    def fetch_all(self) -> list[UserEntity]:
        users = []
        with connections["external_db"].cursor() as cursor:
            cursor.execute("SELECT username, email, first_name, last_name FROM ext_users")
            rows = cursor.fetchall()
            for row in rows:
                users.append(
                    UserEntity(
                        id=0,
                        public_id=None,
                        username=row[0],
                        email=row[1],
                        first_name=row[2],
                        last_name=row[3],
                        bio="Imported from External SQLite"
                    )
                )
        return users
