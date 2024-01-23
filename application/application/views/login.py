from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.permissions import AllowAny

from application.serializers.user import LoginSerializer


class LoginView(KnoxLoginView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
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
        return super(LoginView, self).post(request, format=None)
