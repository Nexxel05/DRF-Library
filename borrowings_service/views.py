from rest_framework import viewsets, mixins

from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingSerializer


class BorrowingListDetailView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.all()

        return queryset
