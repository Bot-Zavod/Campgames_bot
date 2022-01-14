import os
from functools import wraps

from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from bot.admins import ADMINS
from bot.data import text
from bot.password import get_password
from bot.password import write_password
from bot.utils import get_lang
from bot.utils import State
from bot.utils import update_games_in_db
from bot.utils.logs import log_message


GAMES_TABLE_KEY = os.getenv("GAMES_TABLE_KEY")


def restrict_user(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        if update.message.chat.id in ADMINS:
            return func(update, context)
        lang = get_lang(update)
        update.message.reply_text(text["sorry"][lang])
        return None

    return wrapper


@restrict_user
def admin(update: Update, context: CallbackContext):
    log_message(update)
    lang = get_lang(update)
    password = get_password()
    reply_keyboard = [
        [text["update"][lang], text["change_password"][lang]],
        [text["back"][lang]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["hi_boss"][lang] + password, reply_markup=markup)
    return State.ADMIN


@restrict_user
def update_games(update: Update, context: CallbackContext):
    log_message(update)
    msg_text = ""
    try:
        num_rows_deleted, games = update_games_in_db()
        msg_text += f"Deleted {num_rows_deleted} rows\nAdded {games} rows\nFrom table: https://docs.google.com/spreadsheets/d/{GAMES_TABLE_KEY}/"
    except Exception as error:
        msg_text += "Failed with " + str(error)
    update.message.reply_text(msg_text)


@restrict_user
def admin_password(update: Update, context: CallbackContext):
    log_message(update)
    lang = get_lang(update)
    update.message.reply_text(text["send_pass"][lang])
    return State.ADMIN_PASSWORD


@restrict_user
def new_password(update: Update, context: CallbackContext):
    log_message(update)
    lang = get_lang(update)
    write_password(update.message.text)
    update.message.reply_text(text["new_pass"][lang] + update.message.text)
    return admin(update, context)