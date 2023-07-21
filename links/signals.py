import django_rq
from django.db.models.signals import post_save
from django.dispatch import receiver

from .jobs import post_webhook, update_with_ipinfo
from .models import Visit


@receiver(post_save, sender=Visit)
def visit_post_save(sender, **kwargs):
    if kwargs["created"]:
        django_rq.enqueue(update_with_ipinfo, kwargs["instance"])
        django_rq.enqueue(post_webhook, kwargs["instance"])
