from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class IdleTimeoutMiddlewareTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(username="u1", password="p1")

	def test_idle_timeout_redirects_to_login_and_logs_out(self):
		self.client.login(username="u1", password="p1")

		session = self.client.session
		session["last_activity_ts"] = int(timezone.now().timestamp()) - (
			int(getattr(settings, "IDLE_TIMEOUT_SECONDS", 300)) + 1
		)
		session.save()

		resp = self.client.get(reverse("home"))
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(resp.url.startswith(settings.LOGIN_URL))

		self.assertNotIn("_auth_user_id", self.client.session)

	def test_login_page_does_not_redirect_when_timed_out(self):
		self.client.login(username="u1", password="p1")

		session = self.client.session
		session["last_activity_ts"] = int(timezone.now().timestamp()) - (
			int(getattr(settings, "IDLE_TIMEOUT_SECONDS", 300)) + 1
		)
		session.save()

		resp = self.client.get(reverse("login"))
		self.assertEqual(resp.status_code, 200)
