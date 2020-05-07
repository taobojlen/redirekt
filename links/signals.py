import django_rq

from django.db.models.signals import post_save

from .models import Visit
from .jobs import post_webhook, update_with_ipinfo


# Post save signal that notifies of new visits via webhook
def send_webhook_notification(sender, **kwargs):
    if kwargs["created"]:
        django_rq.enqueue(post_webhook, kwargs["instance"])


post_save.connect(
    send_webhook_notification,
    sender=Visit,
    dispatch_uid="post_save_webhook_notification",
)


# Post save signal to look up IP info of a visitor
def get_ipinfo(sender, **kwargs):
    if kwargs["created"]:
        django_rq.enqueue(update_with_ipinfo, kwargs["instance"])


post_save.connect(get_ipinfo, sender=Visit, dispatch_uid="post_save_ipinfo_lookup")
