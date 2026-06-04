from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("users", views.CustomUserViewSet, basename="user")

urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
]
