from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from bot.data import text
from bot.utils import get_lang
from bot.utils import State


async def start_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    reply_keyboard = [
        [text["games"][lang]],
        [text["random"][lang]],
        [text["ask_lang"][lang]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=text["start_games"][lang], reply_markup=markup
    )
    return State.GAMES
