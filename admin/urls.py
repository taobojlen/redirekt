from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin, name="links-admin"),
    path("login/", views.admin_login, name="admin-login"),
    path("create/", views.create_link, name="create-link"),
    path("view/<int:pk>/", views.link_detail, name="link-detail"),
    path("delete/<int:pk>", views.DeleteLink.as_view(), name="delete-link"),
]
