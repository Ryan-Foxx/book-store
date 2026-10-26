from apps.books.api.v1.public.pagination.comment_pagination import CommentPagination
from apps.books.api.v1.public.serializers.comment_serializers import (
    CommentCreateSerializer,
    CommentListSerializer,
)
from apps.books.selectors.comment_selectors import (
    get_public_comment_list_queryset,
    get_public_comment_queryset,
)
from apps.books.services.comment_services import create_comment
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet


# Create your views here.
class CommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):

    pagination_class = CommentPagination

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        return CommentCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["book_pk"] = self.kwargs.get("book_pk")
        return context

    def get_queryset(self):
        book_id = self.kwargs.get("book_pk")

        try:
            book_id = int(book_id)
        except (TypeError, ValueError):
            raise ValidationError({"detail": "Book ID must be a valid integer."})

        if self.action == "list":
            return get_public_comment_list_queryset(book_id=book_id)
        return get_public_comment_queryset()

    def perform_create(self, serializer):

        create_comment(
            user=self.request.user,
            book=serializer.validated_data["book"],
            body=serializer.validated_data["body"],
        )
