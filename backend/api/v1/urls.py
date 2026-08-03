from django.urls import include, path

urlpatterns = [
    # Public Routes
    path("public/", include("apps.books.api.v1.public.urls")),
]
