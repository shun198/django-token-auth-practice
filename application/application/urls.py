from django.urls import include, path
from knox import views as knox_views
from rest_framework_nested.routers import DefaultRouter

from application.views.customer import CustomerViewSet
from application.views.health_check import health_check
from application.views.login import LoginView
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
    path(r"logout", knox_views.LogoutView.as_view(), name="knox_logout"),
]
