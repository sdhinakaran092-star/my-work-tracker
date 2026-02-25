from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from datetime import timedelta

from clinic.models import PendingWork

from .forms import WorkStatusForm
from .models import Attendance, WorkStatus


@login_required
def home(request):
    today = timezone.localdate()

    todays_work_logs_count = WorkStatus.objects.filter(date=today).count()

    todays_attendance = (
        Attendance.objects.filter(timestamp__date=today).order_by("-timestamp").first()
    )
    todays_attendance_status = todays_attendance.status if todays_attendance else None

    monthly_attendance_count = Attendance.objects.filter(
        timestamp__year=today.year,
        timestamp__month=today.month,
    ).count()

    # Attendance trend (latest status per day) for the last 14 days
    trend_days = 14
    start_date = today - timedelta(days=trend_days - 1)
    trend_records = Attendance.objects.filter(
        timestamp__date__gte=start_date,
        timestamp__date__lte=today,
    ).order_by("-timestamp")

    latest_status_by_date = {}
    for record in trend_records:
        record_date = record.timestamp.date()
        if record_date not in latest_status_by_date:
            latest_status_by_date[record_date] = record.status

    attendance_trend = [
        {
            "date": (start_date + timedelta(days=offset)),
            "status": latest_status_by_date.get(start_date + timedelta(days=offset)),
        }
        for offset in range(trend_days)
    ]

    recent_work_statuses = WorkStatus.objects.all()[:5]

    pending_tasks_qs = PendingWork.objects.filter(user=request.user, is_done=False).order_by(
        "due_at", "created_at"
    )
    pending_tasks_count = pending_tasks_qs.count()
    pending_tasks_preview = pending_tasks_qs[:3]

    return render(
        request,
        "My_App/home.html",
        {
            "todays_work_logs_count": todays_work_logs_count,
            "todays_attendance_status": todays_attendance_status,
            "monthly_attendance_count": monthly_attendance_count,
            "recent_work_statuses": recent_work_statuses,
            "pending_tasks_count": pending_tasks_count,
            "pending_tasks_preview": pending_tasks_preview,
            "attendance_trend": attendance_trend,
        },
    )


@login_required
def work_status_list(request):
    statuses = WorkStatus.objects.all()
    return render(request, "My_App/work_status_history.html", {"statuses": statuses})


@login_required
def work_status_add(request):
    if request.method == "POST":
        form = WorkStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("work_status_list")
    else:
        form = WorkStatusForm()

    return render(request, "My_App/add_work_status.html", {"form": form})


@login_required
@ensure_csrf_cookie
def attendance_take(request):
    if request.method == "POST":
        status = request.POST.get("status")

        if status not in (Attendance.Status.PRESENT, Attendance.Status.ABSENT):
            return JsonResponse({"error": "Invalid status"}, status=400)

        photo_file = request.FILES.get("photo")
        if status == Attendance.Status.ABSENT:
            photo_file = None

        attendance = Attendance.objects.create(status=status, photo=photo_file)
        _ = attendance

        messages.success(request, f"Attendance saved: {status}")
        return JsonResponse({"redirect_url": reverse("attendance_history")})

    return render(request, "My_App/attendance_take.html")


@login_required
def attendance_history(request):
    records = Attendance.objects.all()
    return render(request, "My_App/attendance_history.html", {"records": records})
