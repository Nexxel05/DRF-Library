from django.db import models
from django.db.models import Q

from books_service.models import Book
from users_service.models import Customer


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
        Customer,
        related_name="borrowings",
        on_delete=models.CASCADE
    )

    class Meta:
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
