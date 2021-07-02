from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from .database import db_interface
from .etc import text
from .handlers import start
from .utils import State


def admin(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    if str(update.message.chat.username) in ("V_vargan", "lisatkachenko"):
        with open("password.txt", "r") as file:
            password = file.readline()

        update.message.reply_text(text["hi_boss"][lang] + password)

        reply_keyboard = [[text["yes"][lang], text["back"][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text["change"][lang], reply_markup=markup)
        return State.ADMIN

    update.message.reply_text(text["sorry"][lang])
    return start(update, context)


def admin_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    update.message.reply_text(text["send_pass"][lang])
    return State.ADMIN_PASSWORD


def new_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    with open("password.txt", "w") as file:
        file.write(update.message.text)
    update.message.reply_text(text["new_pass"][lang] + update.message.text)
    return admin(update, context)
