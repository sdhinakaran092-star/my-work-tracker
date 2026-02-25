from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/login/"),
        name="logout",
    ),
    path("", views.home, name="home"),
    path("work-status/", views.work_status_list, name="work_status_list"),
    path("history/", views.work_status_list, name="work_status_history"),
    path("add/", views.work_status_add, name="work_status_add"),
    path("attendance/take/", views.attendance_take, name="attendance_take"),
    path("attendance/history/", views.attendance_history, name="attendance_history"),
]
