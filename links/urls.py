from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", views.admin, name="links-admin"),
    path("admin/login/", views.admin_login, name="admin-login"),
    path("admin/create/", views.create_link, name="create-link"),
    path("admin/view/<int:pk>/", views.link_detail, name="link-detail"),
    path("delete/<int:pk>", views.DeleteLink.as_view(), name="delete-link"),
    path("<str:short_id>/", views.redirect_to_destination, name="redirect"),
]
