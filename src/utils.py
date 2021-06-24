from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from .database import db_interface


def get_language(update: Update, context: CallbackContext) -> int:
    """ set user langauge """
    lang = db_interface.get_language(update.message.chat_id)
    if not lang:
        lang = 1
    return lang


def send_msg_with_keyboard(update: Update, msg: str, reply_keyboard: list):
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(msg, reply_markup=markup)
