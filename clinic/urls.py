from django.urls import path

from . import views

urlpatterns = [
    path("", views.pending_list, name="pending_list"),
    path("add/", views.add_pending, name="pending_add"),
    path("<int:pk>/remind/", views.send_reminder, name="pending_remind"),
    path("<int:pk>/done/", views.mark_done, name="pending_done"),
]
