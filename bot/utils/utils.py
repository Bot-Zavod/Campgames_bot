from telegram import ReplyKeyboardMarkup
from telegram import Update

from bot.database import db_interface


def send_msg_with_keyboard(update: Update, msg: str, reply_keyboard: list):
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(msg, reply_markup=markup)


def get_lang(update: Update) -> int:
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    return lang
