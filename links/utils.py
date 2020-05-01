import random
import string

def is_authenticated(request):
    return "authenticated" in request.session and request.session["authenticated"]

def is_bot(user_agent):
    lower = user_agent.lower()
    bot_words = ['bot', 'spider', 'crawler']
    return any(True for b in bot_words if b in lower)

def get_random_short_id():
    chars = string.ascii_letters + string.digits
    return "".join([random.choice(chars) for i in range(6)])
