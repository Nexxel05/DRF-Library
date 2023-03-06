from django.urls import path

from borrowings_service.views import BorrowingListDetailView

borrowings_list = BorrowingListDetailView.as_view(
    actions={
        "get": "list",
    }
)

borrowings_detail = BorrowingListDetailView.as_view(
    actions={
        "get": "retrieve",
    }
)

urlpatterns = [
    path("<int:pk>/", borrowings_detail),
    path("", borrowings_list),
]

app_name = "borrowings_service"
