from django.conf import settings
from django.db import models
from django.db.models import Q

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
