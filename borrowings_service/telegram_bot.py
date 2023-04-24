import os
from datetime import datetime, timedelta

import requests
from django.db.models import Q
from dotenv import load_dotenv

from borrowings_service.models import Borrowing

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_borrowing_notification(borrowing: Borrowing) -> None:
    text = (f"Borrowing id: {borrowing.id}\n"
            f"Borrowing date: {borrowing.borrow_date}\n"
            f"Borrowing expected return date: "
            f"{borrowing.expected_return_date}\n"
            f"Book: {borrowing.book}\n"
            f"Customer: {borrowing.customer}")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=params)


def send_overdue_borrowing_notification() -> None:
    tomorrow = datetime.today() + timedelta(1)
    borrowings = Borrowing.objects.filter(
        Q(actual_return_date__isnull=True) & Q(expected_return_date=tomorrow)
    )

    if borrowings:
        for borrowing in borrowings:
            send_borrowing_notification(borrowing)
    else:
        text = "No borrowings overdue today!"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        requests.post(url, json=params)
