from rest_framework import serializers

from common.validators import FileSizeValidator


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    avatar = serializers.ImageField(required=False, allow_null=True, validators=[FileSizeValidator(5)])
    password = serializers.CharField(write_only=True)


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    avatar = serializers.ImageField(required=False, allow_null=True, validators=[FileSizeValidator(5)])


class UserListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    public_id = serializers.UUIDField()
    username = serializers.CharField()
    first_name = serializers.CharField(allow_null=True)
    last_name = serializers.CharField(allow_null=True)
    bio = serializers.CharField(allow_null=True)
    avatar = serializers.CharField(allow_null=True)
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    public_id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField(allow_null=True)
    last_name = serializers.CharField(allow_null=True)
    bio = serializers.CharField(allow_null=True)
    avatar = serializers.CharField(allow_null=True)
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
