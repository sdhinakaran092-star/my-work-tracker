from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import PendingWork


def get_reminder_recipient(item: PendingWork) -> str | None:
    to_email = (getattr(item, "to_email", "") or "").strip()
    if to_email:
        return to_email

    user_email = (getattr(item.user, "email", "") or "").strip()
    if user_email:
        return user_email

    return None


def build_reminder_email(item: PendingWork) -> tuple[str, str]:
    subject = f"Reminder: {item.title}"
    due_str = timezone.localtime(item.due_at).strftime("%Y-%m-%d %H:%M") if item.due_at else ""
    message = (
        f"Hi {item.user.get_username()},\n\n"
        f"This is a reminder for your pending work:\n\n"
        f"Title: {item.title}\n"
        f"Due: {due_str}\n\n"
        f"Description:\n{item.description or '(no description)'}\n\n"
        f"— My Work Tracker"
    )
    return subject, message


def send_due_reminders() -> int:
    """Send email reminders for overdue pending work.

    Finds PendingWork items where:
    - is_done=False
    - due_at is set and <= now

    Sends an email to the owning user's email.

    Returns:
        int: number of reminder emails sent
    """

    now = timezone.now()
    qs = PendingWork.objects.select_related("user").filter(
        is_done=False,
        due_at__isnull=False,
        due_at__lte=now,
    )

    sent = 0
    for item in qs:
        recipient = get_reminder_recipient(item)
        if not recipient:
            continue

        subject, message = build_reminder_email(item)

        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[recipient],
            fail_silently=False,
        )
        sent += 1

    return sent
