from apps.users.api.v1.views.custom_djoser_viewset import CustomUserViewSet
from apps.users.api.v1.views.logout_views import LogoutView
from apps.users.api.v1.views.user_profile_views import UserProfileView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", CustomUserViewSet, basename="custom-user")

urlpatterns = [
    # User Profile
    path("auth/profile/me/", UserProfileView.as_view(), name="user-profile"),

    # Users (Djoser endpoints powered by CustomUserViewSet)
    path("auth/", include(router.urls)),

    # JWT Authentication Endpoints from Djoser
    path("auth/", include("djoser.urls.jwt")),

    # Logout
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
