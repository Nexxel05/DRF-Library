from typing import Any

import django.core.exceptions
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, exceptions

from rest_framework.test import APIClient
from books_service.tests import sample_book
from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingListSerializer
from users_service.models import Customer

BORROWING_URL = reverse("borrowings_service:borrowing-list")


def sample_customer(**params: Any) -> Customer:
    defaults = {
        "email": "test@test.com",
        "password": "test1234",
    }
    defaults.update(**params)
    return get_user_model().objects.create(**defaults)


def sample_borrowing(**params: Any) -> Borrowing:
    defaults = {
        "borrow_date": "2023-01-01",
        "expected_return_date": "2023-01-03",
        "book": sample_book(),
    }
    defaults.update(**params)
    return Borrowing.objects.create(**defaults)


def detail_url(borrowing_id: int) -> str:
    return reverse("borrowings_service:borrowing-detail", args=[borrowing_id])


def return_url(borrowing_id: int) -> str:
    return reverse("borrowings_service:borrowing-return", args=[borrowing_id])


class BorrowingModelTest(TestCase):
    def test_borrowing_expected_return_date_constraint(self) -> None:
        with self.assertRaises(django.core.exceptions.ValidationError):
            sample_borrowing(
                borrow_date="2023-01-02",
                expected_return_date="2023-01-01",
                customer=sample_customer()
            )

    def test_borrowing_actual_return_date_constraint(self) -> None:
        with self.assertRaises(django.core.exceptions.ValidationError):
            sample_borrowing(
                borrow_date="2023-01-02",
                expected_return_date="2023-01-03",
                actual_return_date="2023-01-01",
                customer=sample_customer()

            )

    def test_borrowing_not_created_with_book_0_inventory(self) -> None:
        book = sample_book(inventory=0)
        with self.assertRaises(exceptions.ValidationError):
            Borrowing.objects.create(
                book=book,
                customer=sample_customer()

            )


class UnauthenticatedUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@t.com",
            "1234test"
        )

        self.client.force_authenticate(self.user)

    def test_list_borrowing_only_created_by_user(self) -> None:
        sample_borrowing(customer=sample_customer())
        sample_borrowing(customer=self.user)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_borrowing_retrieve_allowed(self) -> None:
        borrowing = sample_borrowing(customer=self.user)

        res = self.client.get(detail_url(borrowing.id))

        serializer = BorrowingListSerializer(borrowing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_borrowing_create_by_current_user(self) -> None:
        book = sample_book()
        defaults = {
            "borrow_date": "2023-02-02",
            "expected_return_date": "2023-02-05",
            "book": book.id,
        }

        res = self.client.post(BORROWING_URL, defaults)
        borrowing = Borrowing.objects.get(id=1)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["borrow_date"], defaults["borrow_date"])
        self.assertEqual(borrowing.customer, self.user)

    def test_book_inventory_decreased_when_borrowing_created(self) -> None:
        book = sample_book()

        defaults = {
            "borrow_date": "2023-02-02",
            "expected_return_date": "2023-02-05",
            "book": book.id,
        }

        res = self.client.post(BORROWING_URL, defaults)
        borrowing = Borrowing.objects.get(id=res.data["book"])

        self.assertEqual(res.data["book"], book.id)
        self.assertEqual(borrowing.book.inventory, book.inventory - 1)

    def test_book_inventory_increased_when_book_is_returned(self) -> None:
        book = sample_book()
        borrowing = sample_borrowing(
            book=book,
            customer=self.user
        )
        update = {
            "actual_return_date": "2023-05-05"
        }

        res = self.client.put(return_url(borrowing.id), update)
        borrowing = Borrowing.objects.get(id=borrowing.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(borrowing.book.inventory, book.inventory + 1)

    def test_borrowings_filtering_by_is_active(self) -> None:
        borrowing_due = sample_borrowing(customer=self.user)
        borrowing_not_due = sample_borrowing(
            customer=self.user,
            actual_return_date="2023-01-02",
        )

        serializer_due = BorrowingListSerializer(borrowing_due)
        serializer_not_due = BorrowingListSerializer(borrowing_not_due)

        res = self.client.get(BORROWING_URL, {"is_active": " "})

        self.assertIn(serializer_due.data, res.data)
        self.assertNotIn(serializer_not_due.data, res.data)


class AdminUserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "admin1234",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_all_borrowings(self) -> None:
        sample_borrowing(customer=sample_customer())
        sample_borrowing(customer=self.user)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_delete_borrowing_not_available(self) -> None:
        borrowing = sample_borrowing(customer=self.user)

        res = self.client.delete(detail_url(borrowing.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_borrowings_filtering_by_user_id(self) -> None:
        customer = sample_customer()
        borrowing1 = sample_borrowing(customer=customer)
        borrowing2 = sample_borrowing(customer=self.user)

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        res = self.client.get(BORROWING_URL, {"user_id": customer.id})

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_borrowings_filtering_by_user_id_and_is_active(self) -> None:
        customer = sample_customer()
        borrowing1 = sample_borrowing(customer=customer)
        borrowing2 = sample_borrowing(customer=self.user)
        borrowing3 = sample_borrowing(
            actual_return_date="2023-02-02",
            customer=customer
        )

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)
        serializer3 = BorrowingListSerializer(borrowing3)

        res = self.client.get(BORROWING_URL, {
            "user_id": customer.id,
            "is_active": " "
        })

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
