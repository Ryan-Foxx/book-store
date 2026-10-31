from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound


class CustomUserViewSet(DjoserUserViewSet):
    """
    Subclassed UserViewSet from Djoser to selectively disable unused endpoints:
    - GET /users/ (list)
    - GET, PUT, PATCH, DELETE /users/id/
    - GET, PUT, PATCH, DELETE /users/me/
    """

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        raise NotFound()

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        raise NotFound()

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        raise NotFound()

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        raise NotFound()

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        raise NotFound()

    @extend_schema(exclude=True)
    def me(self, request, *args, **kwargs):
        raise NotFound()
