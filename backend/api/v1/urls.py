from django.urls import include, path

urlpatterns = [
    # Auth Routes
    path("", include("apps.users.api.v1.urls")),

    # Public Routes
    path("public/", include("apps.books.api.v1.public.urls")),

    # Admin Routes
    path("admin/", include("apps.books.api.v1.admin.urls")),
]
