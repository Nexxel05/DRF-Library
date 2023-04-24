from django.db import models


class Book(models.Model):
    class CoverChoice(models.Choices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=63,
        choices=CoverChoice.choices
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}"

    @property
    def daily_fee_usd(self) -> str:
        return f"{self.daily_fee}$"
