import logging

import ipinfo
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

IPINFO_HANDLER = ipinfo.getHandler(settings.IPINFO_TOKEN)


def post_webhook(visit):
    if not settings.WEBHOOK_URL:
        return
    content = 'Someone at IP {} visited your link "{}". See more: {}'.format(
        visit.ip, visit.link, visit.link.get_absolute_url()
    )
    requests.post(settings.WEBHOOK_URL, json={"content": content})


def update_with_ipinfo(visit):
    if not settings.IPINFO_TOKEN:
        return

    # Get details from API
    details = IPINFO_HANDLER.getDetails(visit.ip).all
    logger.warn("IPINFO: %s", details)
    # Update visit
    visit.city = details.get("city")
    visit.country = details.get("country")
    visit.hostname = details.get("hostname")
    visit.latitude = float(details.get("latitude", 0))
    visit.longitude = float(details.get("longitude", 0))
    visit.save(update_fields=["city", "country", "hostname", "latitude", "longitude"])
