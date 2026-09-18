from apps.books.api.v1.public.views.author_viewset import AuthorViewSet
from apps.books.api.v1.public.views.category_viewset import CategoryViewSet
from apps.books.api.v1.public.views.publisher_viewset import PublisherViewSet
from apps.books.api.v1.public.views.translator_viewset import TranslatorViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="public-author")
router.register("translators", TranslatorViewSet, basename="public-translator")
router.register("publishers", PublisherViewSet, basename="public-publisher")
router.register("categories", CategoryViewSet, basename="public-category")

urlpatterns = [
    path("", include(router.urls)),
]
