from apps.books.api.v1.public.views.author_viewset import AuthorViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="public-author")

urlpatterns = [
    path("", include(router.urls)),
]
