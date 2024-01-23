from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from application.serializers.user import LoginSerializer


class LoginView(KnoxLoginView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request=request,
            username=serializer.validated_data["employee_number"],
            password=serializer.validated_data["password"],
        )
        if not user:
            return JsonResponse(
                data={"msg": "社員番号またはパスワードが間違っています"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(request, user)
            token_limit_per_user = self.get_token_limit_per_user()
            if token_limit_per_user is not None:
                now = timezone.now()
                token = request.user.auth_token_set.filter(expiry__gt=now)
                if token.count() >= token_limit_per_user:
                    return Response(
                        {"msg": "ユーザごとに作成できるトークンの上限に達しました"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            token_ttl = self.get_token_ttl()
            user = request.user
            _, token = AuthToken.objects.create(user, token_ttl)
            return Response(
                {
                    "user": user.username,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )


class LogoutView(KnoxLogoutView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        logout(request)
        return HttpResponse()
