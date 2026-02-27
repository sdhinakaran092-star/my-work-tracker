from __future__ import annotations

from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone


class IdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, "user", None) is not None and request.user.is_authenticated:
            now_ts = int(timezone.now().timestamp())
            timeout_seconds = int(getattr(settings, "IDLE_TIMEOUT_SECONDS", 300))

            last_activity_ts = request.session.get("last_activity_ts")
            if isinstance(last_activity_ts, int) and (now_ts - last_activity_ts) > timeout_seconds:
                logout(request)

                login_url = settings.LOGIN_URL
                if request.path != login_url:
                    next_query = urlencode({"next": request.get_full_path()})
                    return redirect(f"{login_url}?{next_query}")

            request.session["last_activity_ts"] = now_ts

        return self.get_response(request)
