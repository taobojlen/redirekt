import random
import string


def is_bot(user_agent):
    lower = user_agent.lower()
    bot_words = ["bot", "spider", "crawler"]
    return any(True for b in bot_words if b in lower)


def get_ray_id():
    chars = string.ascii_lowercase + string.digits
    return "".join([random.choice(chars) for i in range(32)])
