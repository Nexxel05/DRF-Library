from django.contrib import admin

from books_service.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "cover",
        "inventory",
        "daily_fee_usd"
    )
