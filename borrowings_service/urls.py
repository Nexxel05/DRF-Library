from django.urls import path

from borrowings_service.views import BorrowingView

borrowings_list = BorrowingView.as_view(
    actions={
        "get": "list",
        "post": "create"
    }
)

borrowings_detail = BorrowingView.as_view(
    actions={
        "get": "retrieve",
    }
)

urlpatterns = [
    path("<int:pk>/", borrowings_detail),
    path("", borrowings_list),
]

app_name = "borrowings_service"
