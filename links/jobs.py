import ipinfo
import requests

from django.conf import settings

IPINFO_HANDLER = ipinfo.getHandler(settings.IPINFO_TOKEN)


def post_webhook(visit):
    content = 'Someone at IP {} visited your link "{}". See more: {}'.format(
        visit.ip, visit.link, visit.link.get_absolute_url()
    )
    requests.post(settings.WEBHOOK_URL, json={"content": content})


def update_with_ipinfo(visit):
    # Get details from API
    details = IPINFO_HANDLER.getDetails(visit.ip).all
    # Update visit
    visit.city = details.get("city")
    visit.country = details.get("country")
    visit.hostname = details.get("hostname")
    visit.latitude = float(details.get("latitude"))
    visit.longitude = float(details.get("longitude"))
    visit.save(update_fields=["city", "country", "hostname", "latitude", "longitude"])
