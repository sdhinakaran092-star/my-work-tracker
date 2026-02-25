from django.conf import settings
from django.db import models


class PendingWork(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	due_at = models.DateTimeField(blank=True, null=True)
	to_email = models.EmailField(blank=True, null=True)
	is_done = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["due_at", "-created_at", "-id"]

	def __str__(self) -> str:
		return self.title

# Create your models here.
