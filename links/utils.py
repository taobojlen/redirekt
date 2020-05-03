def is_bot(user_agent):
    lower = user_agent.lower()
    bot_words = ["bot", "spider", "crawler"]
    return any(True for b in bot_words if b in lower)
