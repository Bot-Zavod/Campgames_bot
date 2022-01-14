import os
from functools import wraps

from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from bot.etc import text
from bot.handlers import start
from bot.utils import get_lang
from bot.utils import State
from bot.utils import update_games_in_db

ADMINS = set(os.getenv("ADMINS", "").split(" "))


def restrict_user(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        username = str(update.message.chat.username).lower()
        if username in ADMINS:
            return func(update, context)
        lang = get_lang(update)
        update.message.reply_text(text["sorry"][lang])
        return start(update, context)

    return wrapper


@restrict_user
def admin(update: Update, context: CallbackContext):
    lang = get_lang(update)
    with open("password.txt", "r") as file:
        password = file.readline()
    reply_keyboard = [
        [text["update"][lang], text["change_password"][lang]],
        [text["back"][lang]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["hi_boss"][lang] + password, reply_markup=markup)
    return State.ADMIN


@restrict_user
def update_games(update: Update, context: CallbackContext):
    msg_text = ""
    try:
        num_rows_deleted, games = update_games_in_db()
        msg_text += f"Deleted {num_rows_deleted} rows\nAdded {games} rows"
    except Exception as error:
        msg_text += "Failed with " + str(error)
    update.message.reply_text(msg_text)


@restrict_user
def admin_password(update: Update, context: CallbackContext):
    lang = get_lang(update)
    update.message.reply_text(text["send_pass"][lang])
    return State.ADMIN_PASSWORD


@restrict_user
def new_password(update: Update, context: CallbackContext):
    lang = get_lang(update)
    with open("password.txt", "w") as file:
        file.write(update.message.text)
    update.message.reply_text(text["new_pass"][lang] + update.message.text)
    return admin(update, context)
