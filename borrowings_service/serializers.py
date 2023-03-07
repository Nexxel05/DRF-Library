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


class BorrowingReturnSerializer(BorrowingSerializer):
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
        read_only_fields = (
            "borrow_date",
            "expected_return_date",
            "book",
            "customer"
        )

    def update(self, instance, validated_data):
        if not instance.actual_return_date:
            if validated_data.get("actual_return_date") < instance.borrow_date:
                raise serializers.ValidationError(
                    "Actual return date can not be earlier than borrow date"
                )
            instance.actual_return_date = validated_data.get(
                "actual_return_date", instance.actual_return_date
            )
            instance.book.inventory += 1
            instance.book.save()
            instance.save()
        return instance
