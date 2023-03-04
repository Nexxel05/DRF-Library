from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from books_service.models import Book
from books_service.serializers import BookSerializer, BookListDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = [IsAdminUser, ]
            return BookListDetailSerializer
        return BookSerializer
