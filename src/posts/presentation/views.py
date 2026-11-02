from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.mixins import SerializerMixin
from posts.application.use_cases import (
    CreatePost,
    DeletePost,
    GetPost,
    ListPosts,
    UpdatePost,
)
from posts.domain.entities import Post as PostEntity
from posts.domain.exceptions import PostNotFoundError
from posts.infrastructure.repositories import DjangoPostRepository
from .serializers import (
    CreatePostSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostUpdateSerializer,
)


class PostListView(SerializerMixin, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer

    def get(self, request, *args, **kwargs):
        use_case = ListPosts(DjangoPostRepository())
        posts = use_case.execute()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class PostCreateView(SerializerMixin, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        entity = PostEntity(
            public_id=None,
            author_id=request.user.id,
            author_username=request.user.username,
            title=data["title"],
            body=data["body"],
        )

        use_case = CreatePost(DjangoPostRepository())
        created = use_case.execute(entity)

        return Response(
            PostDetailSerializer(created).data,
            status=status.HTTP_201_CREATED,
        )


class PostDetailView(SerializerMixin, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostDetailSerializer

    def get(self, request, *args, **kwargs):
        public_id = kwargs.get("public_id")

        use_case = GetPost(DjangoPostRepository())
        try:
            post = use_case.execute(public_id)
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        except PostNotFoundError:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PostUpdateView(SerializerMixin, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUpdateSerializer

    def patch(self, request, *args, **kwargs):
        public_id = kwargs.get("public_id")

        get_use_case = GetPost(DjangoPostRepository())
        try:
            post = get_use_case.execute(public_id)
        except PostNotFoundError:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.author_id != request.user.id:
            raise PermissionDenied("You can only update your own posts.")

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        update_use_case = UpdatePost(DjangoPostRepository())
        try:
            updated_post = update_use_case.execute(
                public_id=public_id,
                author_id=request.user.id,
                **serializer.validated_data
            )
            return Response(PostDetailSerializer(updated_post).data)
        except PostNotFoundError:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        public_id = kwargs.get("public_id")

        get_use_case = GetPost(DjangoPostRepository())
        try:
            post = get_use_case.execute(public_id)
        except PostNotFoundError:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.author_id != request.user.id:
            raise PermissionDenied("You can only delete your own posts.")

        delete_use_case = DeletePost(DjangoPostRepository())
        try:
            delete_use_case.execute(public_id, request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostNotFoundError:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
