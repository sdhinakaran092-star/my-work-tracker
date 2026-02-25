from django.contrib import admin

from .models import PendingWork


@admin.register(PendingWork)
class PendingWorkAdmin(admin.ModelAdmin):
	list_display = ("title", "user", "to_email", "due_at", "is_done", "created_at")
	list_filter = ("is_done", "due_at", "created_at")
	search_fields = ("title", "description", "to_email", "user__username", "user__email")
