from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import (
    IsAnonymousPermission,
    IsNotSelfPermission,
    IsSameUserPermission,
)
from users.application.use_cases import (
    DeleteUser,
    FollowUser,
    GetUserFollowers,
    GetUserFollowing,
    GetUserProfile,
    ListUsers,
    RegisterUser,
    UnfollowUser,
    UpdateUser,
)
from users.domain.exceptions import UserNotFoundError
from users.infrastructure.repositories import DjangoUserRepository
from .serializers import (
    UserListSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
)
from users.infrastructure.repositories import SqliteExternalUserRepository
from users.application.use_cases import SyncUsersFromExternalDB


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        use_case = ListUsers(DjangoUserRepository())
        users_entity = use_case.execute()
        return Response(UserListSerializer(users_entity, many=True).data)


class SyncUsersView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        use_case = SyncUsersFromExternalDB(
            external_repo=SqliteExternalUserRepository(),
            main_repo=DjangoUserRepository()
        )
        try:
            count = use_case.execute()
            return Response({"message": f"{count} users synced successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAnonymousPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = RegisterUser(DjangoUserRepository())
        try:
            user_entity = use_case.execute(**serializer.validated_data)
            return Response(UserProfileSerializer(user_entity).data,status=status.HTTP_201_CREATED,)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST,)


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        use_case = GetUserProfile(DjangoUserRepository())
        try:
            user_entity = use_case.execute(username)
            return Response(UserProfileSerializer(user_entity).data)
        except UserNotFoundError:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND,)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsSameUserPermission]

    def update(self, request, username, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        use_case = UpdateUser(DjangoUserRepository())
        try:
            user_entity = use_case.execute(username, **serializer.validated_data)
            return Response(UserProfileSerializer(user_entity).data)
        except UserNotFoundError:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND,)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSameUserPermission]

    def delete(self, request, username, *args, **kwargs):
        use_case = DeleteUser(DjangoUserRepository())
        try:
            use_case.execute(username)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserNotFoundError:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND,)


class UserFollowView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsNotSelfPermission]

    def post(self, request, username):
        try:
            FollowUser(DjangoUserRepository()).execute(
                follower_username=request.user.username, 
                following_username=username
            )
            return Response({"detail": "User followed."}, status=status.HTTP_200_OK)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except UserNotFoundError:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class UserUnfollowView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsNotSelfPermission]

    def post(self, request, username):
        try:
            UnfollowUser(DjangoUserRepository()).execute(
                follower_username=request.user.username, 
                following_username=username
            )
            return Response({"detail": "User unfollowed."}, status=status.HTTP_200_OK)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except UserNotFoundError:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class UserFollowerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer

    def get(self, request, username, *args, **kwargs):
        use_case = GetUserFollowers(DjangoUserRepository())
        followers = use_case.execute(username)
        return Response(UserListSerializer(followers, many=True).data)


class UserFollowingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer

    def get(self, request, username, *args, **kwargs):
        use_case = GetUserFollowing(DjangoUserRepository())
        following = use_case.execute(username)
        return Response(UserListSerializer(following, many=True).data)
