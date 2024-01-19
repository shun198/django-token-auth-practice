from rest_framework import serializers

from application.models import User


class UserSerializer(serializers.ModelSerializer):
    """ユーザ用シリアライザ"""

    class Meta:
        model = User
        fields = ["id", "employee_number", "username", "email", "role"]
        read_only_fields = ["id", "created_at", "updated_at"]


class LoginSerializer(serializers.ModelSerializer):
    employee_number = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["employee_number", "password"]


class CreateTokenSerializer(serializers.Serializer):
    """ログイン用シリアライザ"""

    user_id = serializers.UUIDField()


class EmailSerializer(serializers.Serializer):
    """Email用シリアライザ"""

    email = serializers.EmailField(max_length=255)
