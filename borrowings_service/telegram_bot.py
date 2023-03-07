import os

import requests
from dotenv import load_dotenv

from borrowings_service.models import Borrowing

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_borrowing_notification(borrowing: Borrowing):

    text = f"Borrowing id: {borrowing.id}\n" \
           f"Borrowing date: {borrowing.borrow_date}\n" \
           f"Borrowing expected return date: {borrowing.expected_return_date}\n" \
           f"Book: {borrowing.book}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(url, json=params)
