from borrowings_service.telegram_bot import send_overdue_borrowing_notification


def borrowings_daily_overdue() -> None:
    send_overdue_borrowing_notification()
