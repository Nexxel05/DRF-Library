from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrowing.objects.all()

        is_active = self.request.query_params.get("is_active")

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        if self.request.user.is_staff:

            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(customer__id=user_id)

            return queryset

        queryset = queryset.filter(customer=self.request.user)

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
