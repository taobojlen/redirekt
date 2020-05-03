import random
import string


def is_authenticated(request):
    return "authenticated" in request.session and request.session["authenticated"]


def get_random_short_id():
    chars = string.ascii_letters + string.digits
    return "".join([random.choice(chars) for i in range(6)])
