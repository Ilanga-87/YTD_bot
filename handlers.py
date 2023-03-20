async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! I'm a bot that can help you to find the best place to eat food. "
        "I can help you to find the best place to eat food. "
    )
