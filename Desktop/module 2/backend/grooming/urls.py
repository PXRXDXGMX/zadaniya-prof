from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page),
    path("user/", views.user_page),
    path("groom/", views.groom_page),
    path("api/auth/register", views.register_view),
    path("api/auth/login", views.login_view),
    path("api/auth/logout", views.logout_view),
    path("api/auth/me", views.me_view),
    path("api/public/completed", views.completed_requests_view),
    path("api/user/requests", views.user_requests_view),
    path("api/user/requests/<int:request_id>", views.delete_user_request_view),
    path("api/groom/requests", views.admin_requests_view),
    path("api/groom/requests/<int:request_id>/status", views.admin_update_status_view),
]
