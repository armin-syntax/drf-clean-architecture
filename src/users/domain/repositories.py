from __future__ import annotations
from abc import ABC, abstractmethod

from .entities import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> UserEntity:
        pass

    @abstractmethod
    def list(self) -> list[UserEntity]:
        pass

    @abstractmethod
    def create(self, username: str, email: str, password: str, **kwargs) -> UserEntity:
        pass

    @abstractmethod
    def update(self, username: str, **kwargs) -> UserEntity:
        pass

    @abstractmethod
    def delete(self, username: str) -> None:
        pass

    @abstractmethod
    def follow(self, follower_username: str, following_username: str) -> None:
        pass

    @abstractmethod
    def unfollow(self, follower_username: str, following_username: str) -> None:
        pass

    @abstractmethod
    def get_followers(self, username: str) -> list[UserEntity]:
        pass

    @abstractmethod
    def get_following(self, username: str) -> list[UserEntity]:
        pass

    @abstractmethod
    def check_username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def check_email_exists(self, email: str) -> bool:
        pass


class ExternalUserRepository(ABC):
    @abstractmethod
    def fetch_all(self) -> list[UserEntity]:
        pass
