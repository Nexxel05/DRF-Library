from rest_framework import viewsets

from books_service.models import Book
from books_service.serializers import BookSerializer, BookLisDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookLisDetailSerializer
        return BookSerializer
