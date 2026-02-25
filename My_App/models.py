from django.db import models


class WorkStatus(models.Model):
	date = models.DateField(auto_now_add=True)
	work_done = models.TextField()

	class Meta:
		ordering = ["-date", "-id"]

	def __str__(self) -> str:
		return f"{self.date}: {self.work_done[:50]}"


class Attendance(models.Model):
	class Status(models.TextChoices):
		PRESENT = "Present", "Present"
		ABSENT = "Absent", "Absent"

	status = models.CharField(max_length=10, choices=Status.choices)
	timestamp = models.DateTimeField(auto_now_add=True)
	photo = models.ImageField(upload_to="attendance_photos/", blank=True, null=True)

	class Meta:
		ordering = ["-timestamp", "-id"]

	def __str__(self) -> str:
		return f"{self.timestamp:%Y-%m-%d %H:%M} - {self.status}"
