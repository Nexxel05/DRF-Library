from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from books_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book,
        related_name="borrowings",
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrowings",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("borrow_date",)
        constraints = [
            models.CheckConstraint(
                check=Q(borrow_date__lte=models.F("expected_return_date")),
                name="borrow_date_lte_expected_return_date",
            ),
            models.CheckConstraint(
                check=Q(borrow_date__lte=models.F("actual_return_date")),
                name="borrow_date_lte_actual_return_date"
            )
        ]

    @staticmethod
    def validate_book_inventory(inventory: int, error_to_raise: Any) -> None:
        if inventory == 0:
            raise error_to_raise(
                "Inventory of this book is 0, it can not be borrowed"
            )

    def clean(self) -> None:
        Borrowing.validate_book_inventory(self.book.inventory, ValidationError)

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: object = None,
            update_fields: list = None
    ) -> callable:
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )
