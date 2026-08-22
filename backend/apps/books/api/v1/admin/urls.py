from apps.books.api.v1.admin.views.author_viewset import AuthorViewSet
from apps.books.api.v1.admin.views.award_viewset import AwardViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="admin-author")
router.register("awards", AwardViewSet, basename="admin-award")

urlpatterns = [
    path("", include(router.urls)),
]
