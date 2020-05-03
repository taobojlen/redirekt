from django.urls import path

from . import views

urlpatterns = [
    path("<str:short_id>/", views.redirect_to_destination, name="redirect"),
]
