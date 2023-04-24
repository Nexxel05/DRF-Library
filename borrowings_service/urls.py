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

borrowings_return = BorrowingView.as_view(
    actions={
        "get": "retrieve",
        "put": "update",
    }
)

urlpatterns = [
    path("<int:pk>/", borrowings_detail, name="borrowing-detail"),
    path("<int:pk>/return/", borrowings_return, name="borrowing-return"),
    path("", borrowings_list, name="borrowing-list"),
]

app_name = "borrowings_service"
