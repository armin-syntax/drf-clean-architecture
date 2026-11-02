# Django discovers models through this module.
from users.infrastructure.models import User, Follow


__all__ = ["User", "Follow"]
