from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.admin, name="links-admin"),
    path("create/", views.create_link, name="create-link"),
    path("view/<int:pk>/", views.link_detail, name="link-detail"),
    path("delete/<int:pk>", views.DeleteLink.as_view(), name="delete-link"),
    path("login/", auth_views.LoginView.as_view()),
    path("logout/", auth_views.LogoutView.as_view()),
    path(
        "password_change/", auth_views.PasswordChangeView.as_view(success_url="/admin/")
    ),
]
