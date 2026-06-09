from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

router = DefaultRouter()
router.register("users", views.CustomUserViewSet, basename="user")

urlpatterns = [
    # Users (Djoser)
    path("auth/", include(router.urls)),
    # JWT
    path("auth/jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # Logout
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
]
