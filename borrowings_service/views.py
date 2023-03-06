from rest_framework import viewsets, mixins

from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingListSerializer,
    BorrowingCreateSerializer
)


class BorrowingView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin
):
    serializer_class = BorrowingListSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.all()

        return queryset

    def get_serializer_class(self):
        serializer_dict = {
            "list": BorrowingListSerializer,
            "retrieve": BorrowingListSerializer,
            "create": BorrowingCreateSerializer
        }
        return serializer_dict.get(self.action)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
