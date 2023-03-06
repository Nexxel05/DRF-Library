import datetime

from rest_framework import serializers

from books_service.serializers import BookListDetailSerializer
from borrowings_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookListDetailSerializer(read_only=True)
    borrow_date = serializers.DateField(initial=datetime.datetime.today())

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "customer"
        )
