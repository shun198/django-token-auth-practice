from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from application.views.customer import CustomerViewSet
from application.views.health_check import health_check
from application.views.login import LoginView, LogoutView
from application.views.sms import SmsViewSet
from application.views.user import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"", SmsViewSet, basename="sms")
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"health", health_check, name="health_check"),
    path(r"login", LoginView.as_view(), name="knox_login"),
    path(r"logout", LogoutView.as_view(), name="knox_logout"),
]
