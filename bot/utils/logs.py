""" logger config """
from loguru import logger
from telegram import Update


def log_message(update: Update):
    """Logging user id and message"""

    if hasattr(update, "message") and hasattr(update.message, "chat"):
        logger.bind(chat_id=update.message.chat.id).opt(depth=1).info(
            update.message.text
        )
