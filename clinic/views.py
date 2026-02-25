from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.conf import settings

from .forms import PendingWorkForm
from .models import PendingWork
from .utils import get_reminder_recipient, build_reminder_email

@login_required
def pending_list(request):
	tasks = (
		PendingWork.objects.filter(user=request.user, is_done=False)
		.order_by("due_at", "created_at")
	)
	return render(request, "clinic/pending_list.html", {"tasks": tasks})


@login_required
def add_pending(request):
	if request.method == "POST":
		form = PendingWorkForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.user = request.user

			# If due_at is provided via datetime-local input without timezone,
			# Django will interpret it as naive; convert to aware in current TZ.
			if task.due_at and timezone.is_naive(task.due_at):
				task.due_at = timezone.make_aware(task.due_at, timezone.get_current_timezone())

			task.save()
			messages.success(request, "Pending work added.")
			return redirect("pending_list")
	else:
		form = PendingWorkForm()

	return render(request, "clinic/add_pending.html", {"form": form})


@login_required
def mark_done(request, pk: int):
	if request.method != "POST":
		raise Http404()

	task = get_object_or_404(PendingWork, pk=pk, user=request.user)
	task.is_done = True
	task.save(update_fields=["is_done"])
	messages.success(request, "Marked as done.")
	return redirect("pending_list")


@login_required
def send_reminder(request, pk: int):
	if request.method != "POST":
		raise Http404()

	task = get_object_or_404(PendingWork, pk=pk, user=request.user, is_done=False)
	recipient = get_reminder_recipient(task)
	if not recipient:
		messages.error(request, "No email found. Please add your email or enter To Email.")
		return redirect("pending_list")

	subject, message = build_reminder_email(task)
	send_mail(
		subject=subject,
		message=message,
		from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
		recipient_list=[recipient],
		fail_silently=False,
	)

	messages.success(request, f"Reminder sent to {recipient}")
	return redirect("pending_list")
