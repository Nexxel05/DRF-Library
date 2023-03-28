from django_q.models import Schedule


Schedule.objects.create(
    func="borrowings_service.telegram_bot.send_overdue_borrowing_notification",
    name="Daily borrowings overdue notification",
    schedule_type=Schedule.DAILY,
)
