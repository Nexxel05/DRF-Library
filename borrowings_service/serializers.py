import datetime

from rest_framework import serializers

from books_service.serializers import BookListDetailSerializer
from borrowings_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "customer"
        )


class BorrowingCreateSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        exclude = ("customer",)

    def create(self, validated_data):
        borrowing = Borrowing.objects.create(**validated_data)
        book = borrowing.book
        book.inventory -= 1
        book.save()
        return borrowing

    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs)
        if data["book"].inventory == 0:
            raise serializers.ValidationError(
                f"The {data['book'].title} is out of stock"
            )
        return data


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListDetailSerializer(read_only=True)
