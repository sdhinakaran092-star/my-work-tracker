from django.contrib import admin

from .models import Attendance, WorkStatus


@admin.register(WorkStatus)
class WorkStatusAdmin(admin.ModelAdmin):
	list_display = ("date", "work_done")
	search_fields = ("work_done",)
	list_filter = ("date",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ("timestamp", "status", "photo")
	list_filter = ("status", "timestamp")
