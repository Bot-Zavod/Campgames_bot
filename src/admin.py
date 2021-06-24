from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from .etc import text
from .handlers import start
from .states_range import State
from .utils import get_language


def admin(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    if str(update.message.chat.username) in ("V_vargan", "lisatkachenko"):
        file_name = r"password.txt"
        with open(file_name, "r") as file:
            password = file.readline()
            file.close()

        update.message.reply_text(text["hi_boss"][lang] + password)

        reply_keyboard = [[text["yes"][lang], text["back"][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text["change"][lang], reply_markup=markup)
        return State.ADMIN

    update.message.reply_text(text["sorry"][lang])
    return start(update, context)


def admin_password(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    update.message.reply_text(text["send_pass"][lang])
    return State.ADMIN_PASSWORD


def new_password(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    with open("password.txt", "w") as file:
        file.write(update.message.text)
    update.message.reply_text(text["new_pass"][lang] + update.message.text)
    return admin(update, context)
