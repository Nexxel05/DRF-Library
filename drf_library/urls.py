from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include(
        "books_service.urls", namespace="books_service"
    )),
    path("users/", include(
        "users_service.urls", namespace="users_service"
    )),
    path("borrowings/", include(
        "borrowings_service.urls", namespace="borrowings_service"
    )),
    path("api/schema/", SpectacularAPIView.as_view(), name='schema'),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger"
    ),
]
