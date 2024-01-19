from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from application.models.user import User
from application.serializers.user import (
    CreateTokenSerializer,
    LoginSerializer,
    UserSerializer,
)
from project.settings.environment import django_settings


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateTokenViewSet(LoginView):
    permission_classes = [AllowAny]
    serializer_class = CreateTokenSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"msg": "ユーザーごとの許容されるトークンの最大数を超えました"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        expiry = self.get_token_ttl()
        user = get_object_or_404(
            User,
            pk=serializer.validated_data.get("user_id"),
        )
        _, token = AuthToken.objects.create(user, expiry)
        return Response(
            {"msg": "トークンを発行しました", "token": token},
            status=status.HTTP_200_OK,
        )


class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """ユーザのログイン"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee_number = serializer.validated_data.get("employee_number")
        password = serializer.validated_data.get("password")
        user = authenticate(employee_number=employee_number, password=password)
        if not user:
            return JsonResponse(
                data={"msg": "社員番号またはパスワードが間違っています"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(request, user)
            return JsonResponse(data={"role": user.Role(user.role).name})

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """ユーザのログアウト"""
        logout(request)
        return HttpResponse()


if django_settings.DJANGO_SETTINGS_MODULE == "project.settings.local":
    from drf_spectacular.utils import (
        OpenApiExample,
        OpenApiResponse,
        extend_schema,
    )

    extend_schema(
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                "login request",
                value={
                    "employee_number": "00000001",
                    "password": "test",
                },
                request_only=True,
                description="ログインユーザー",
            ),
        ],
        responses=OpenApiResponse(
            status.HTTP_200_OK,
            examples=[
                OpenApiExample(
                    "login response",
                    value={
                        "role": "MANAGEMENT",
                    },
                    response_only=True,
                    description="ログインユーザー権限",
                )
            ],
            description="ログインが成功しました",
        ),
        summary="ユーザーログイン",
    )(LoginViewSet.login)
