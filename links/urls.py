from django.urls import path

from . import views

urlpatterns = [
    path("update/", views.update_visit, name="update-visit"),
    path("<str:short_id>/", views.redirect_to_destination, name="redirect"),
]
