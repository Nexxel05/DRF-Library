from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books_service.models import Book
from books_service.serializers import BookListDetailSerializer

BOOK_URL = reverse("books_service:book-list")


def sample_book(**params: Any) -> Book:
    defaults = {
        "title": "test book",
        "author": "test author",
        "cover": "Hard",
        "inventory": 1,
        "daily_fee": "0.10"
    }

    defaults.update(**params)

    return Book.objects.create(**defaults)


def detail_url(book_id: int) -> str:
    return reverse("books_service:book-detail", args=[book_id])


class UnauthenticatedUserMovieTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_not_required(self) -> None:
        res = self.client.get(BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_book_not_allowed(self) -> None:
        data = {
            "title": "book",
            "author": "author",
            "cover": "Hard",
            "inventory": 1,
            "daily_fee": "0.10"
        }
        res = self.client.post(BOOK_URL, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test1234",
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self) -> None:
        sample_book()
        sample_book()
        books = Book.objects.all()

        serializer = BookListDetailSerializer(books, many=True)
        res = self.client.get(BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_with_usd_daily_fee(self) -> None:
        book = sample_book()

        res = self.client.get(detail_url(book.id))
        serializer = BookListDetailSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_not_allowed(self) -> None:
        data = {
            "title": "book",
            "author": "author",
            "cover": "Hard",
            "inventory": 1,
            "daily_fee": "0.10"
        }
        res = self.client.post(BOOK_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_book_not_allowed(self) -> None:
        book = sample_book()

        res = self.client.put(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_book_not_allowed(self) -> None:
        book = sample_book()

        res = self.client.patch(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_not_allowed(self) -> None:
        book = sample_book()

        res = self.client.delete(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "admin1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book_allowed(self) -> None:
        data = {
            "title": "book",
            "author": "author",
            "cover": "Hard",
            "inventory": 1,
            "daily_fee": "0.10"
        }
        res = self.client.post(BOOK_URL, data)
        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["title"], book.title)

    def test_put_book_allowed(self) -> None:
        book = sample_book()
        data = {
            "title": "updated book",
            "author": "updated author",
            "cover": "Hard",
            "inventory": 2,
            "daily_fee": "0.30"
        }
        res = self.client.put(detail_url(book.id), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], res.data["title"])

    def test_delete_book_allowed(self) -> None:
        book = sample_book()

        res = self.client.delete(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
