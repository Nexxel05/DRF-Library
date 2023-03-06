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
        Borrowing.validate_book_inventory(data["book"].inventory, serializers.ValidationError)
        return data


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListDetailSerializer(read_only=True)
