from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from bot.data import text
from bot.utils import State

# from bot.utils import get_lang


async def start_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # lang = get_lang(update)
    """reply_keyboard = [
        [text["games"][lang]],
        [text["random"][lang]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=text["start_games"][lang], reply_markup=markup
    )"""

    reply_keyboard = [
        [text["games"]],
        [text["random"]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=text["start_games"], reply_markup=markup
    )
    return State.GAMES


def change_indent(description: str) -> str:
    """changes indent in description and makes first line bold"""

    index = description.find("\n")

    if index == -1:
        return description

    description = f"<b>{description[:index]}</b>" + "\n\n" + description[index:].strip()
    return description
