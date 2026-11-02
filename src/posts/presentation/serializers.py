from rest_framework import serializers


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=2000)


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    body = serializers.CharField(max_length=2000, required=False)


class PostListSerializer(serializers.Serializer):
    public_id = serializers.UUIDField()
    author_id = serializers.IntegerField()
    author_username = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField()
    created_at = serializers.DateTimeField()


class PostDetailSerializer(serializers.Serializer):
    public_id = serializers.UUIDField()
    author_id = serializers.IntegerField()
    author_username = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
