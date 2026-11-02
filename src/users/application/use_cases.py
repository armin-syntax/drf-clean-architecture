from users.domain.entities import UserEntity
from users.domain.repositories import UserRepository


class RegisterUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, username: str, email: str, password: str, **kwargs) -> UserEntity:
        if self.repository.check_username_exists(username):
            raise ValueError("This username is already taken.")
            
        if self.repository.check_email_exists(email):
            raise ValueError("This email is already registered.")
            
        return self.repository.create(username, email, password, **kwargs)


class ListUsers:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self) -> list[UserEntity]:
        return self.repository.list()


class GetUserProfile:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, username: str) -> UserEntity:
        return self.repository.get_by_username(username)


class UpdateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, username: str, **kwargs) -> UserEntity:
        return self.repository.update(username, **kwargs)


class DeleteUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, username: str) -> None:
        self.repository.delete(username)


class FollowUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, follower_username: str, following_username: str) -> None:
        self.repository.follow(follower_username, following_username)


class UnfollowUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, follower_username: str, following_username: str) -> None:
        self.repository.unfollow(follower_username, following_username)


class GetUserFollowers:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, username: str) -> list[UserEntity]:
        return self.repository.get_followers(username)


class GetUserFollowing:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, username: str) -> list[UserEntity]:
        return self.repository.get_following(username)
