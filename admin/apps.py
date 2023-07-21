from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = "admin"
    default_site = "django.contrib.admin.sites.AdminSite"
