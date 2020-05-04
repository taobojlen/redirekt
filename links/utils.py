import random
import requests
import string

from django.conf import settings


def is_bot(user_agent):
    lower = user_agent.lower()
    bot_words = ["bot", "spider", "crawler"]
    return any(True for b in bot_words if b in lower)


def get_ray_id():
    chars = string.ascii_lowercase + string.digits
    return "".join([random.choice(chars) for i in range(32)])


def deep_get(d, keys):
    if not keys or d is None:
        return d
    return deep_get(d.get(keys[0]), keys[1:])


def post_webhook(visit):
    content = "Someone at IP {} visited your link \"{}\". See more: {}".format(visit.ip, visit.link, visit.link.get_absolute_url())
    requests.post(settings.WEBHOOK_URL, json={"content": content})
