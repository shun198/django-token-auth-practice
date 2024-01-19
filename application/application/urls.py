from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from application.views.customer import CustomerViewSet
from application.views.health_check import health_check
from application.views.login import CreateTokenViewSet, LoginViewSet
from application.views.sms import SmsViewSet
from application.views.user import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"", SmsViewSet, basename="sms")
router.register(r"customer", CustomerViewSet, basename="customer")
router.register(r"", LoginViewSet, basename="login")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"health", health_check, name="health_check"),
    path(r"create_token", CreateTokenViewSet.as_view(), name="create_token"),
]
