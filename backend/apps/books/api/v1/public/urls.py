from apps.books.api.v1.public.views.author_viewset import AuthorViewSet
from apps.books.api.v1.public.views.book_viewset import BookViewSet
from apps.books.api.v1.public.views.category_viewset import CategoryViewSet
from apps.books.api.v1.public.views.comment_viewset import CommentViewSet
from apps.books.api.v1.public.views.publisher_viewset import PublisherViewSet
from apps.books.api.v1.public.views.translator_viewset import TranslatorViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register("authors", AuthorViewSet, basename="public-author")
router.register("translators", TranslatorViewSet, basename="public-translator")
router.register("publishers", PublisherViewSet, basename="public-publisher")
router.register("categories", CategoryViewSet, basename="public-category")
router.register("books", BookViewSet, basename="public-book")

# ------------------- Create Nested Routers ↓ -------------------
books_router = routers.NestedDefaultRouter(router, "books", lookup="book")
books_router.register("comments", CommentViewSet, basename="public-book-comment")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(books_router.urls)),
]
