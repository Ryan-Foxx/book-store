from apps.books.api.v1.admin.views.author_viewset import AuthorViewSet
from apps.books.api.v1.admin.views.award_viewset import AwardViewSet
from apps.books.api.v1.admin.views.publisher_viewset import PublisherViewSet
from apps.books.api.v1.admin.views.translator_viewset import TranslatorViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="admin-author")
router.register("awards", AwardViewSet, basename="admin-award")
router.register("translators", TranslatorViewSet, basename="admin-translator")
router.register("publishers", PublisherViewSet, basename="admin-publisher")

urlpatterns = [
    path("", include(router.urls)),
]
