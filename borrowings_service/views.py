from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.serializers import Serializer

from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingListSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer
)


class BorrowingView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
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

    def get_serializer_class(self) -> Serializer:
        serializer_dict = {
            "list": BorrowingListSerializer,
            "retrieve": BorrowingListSerializer,
            "create": BorrowingCreateSerializer,
            "update": BorrowingReturnSerializer,
        }
        return serializer_dict.get(self.action, BorrowingListSerializer)

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(customer=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="Search by user id",
                type=int
            ),
            OpenApiParameter(
                name="is_active",
                description="Search by pending borrowings",
            )
        ]
    )
    def list(
            self,
            request: Request,
            *args: list,
            **kwargs: list
    ) -> callable:
        return super().list(request, *args, **kwargs)
