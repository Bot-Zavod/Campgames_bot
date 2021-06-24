import logging
from random import randint

from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from .database import db_interface
from .etc import games
from .etc import text
from .states_range import State
from .utils import get_language


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = get_language(update, context)

    update.message.reply_text(text["start"][lang], reply_markup=ReplyKeyboardRemove())
    db_lang = db_interface.get_language(chat_id)
    if db_lang is None:
        return ask_lang(update, context)
    if not db_interface.check_user(chat_id):
        return ask_password(update, context)
    return start_query(update, context)


def ask_password(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    update.message.reply_text(text["ask_pass"][lang])
    return State.CHECK_PASSWORD


def check_password(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    file_name = r"password.txt"
    with open(file_name, "r") as file:
        password = file.readline()
        file.close()

    if update.message.text == password:
        db_interface.authorize_user(update.message.chat_id)
        update.message.reply_text(text["pass_success"][lang])
        return start_query(update, context)

    update.message.reply_text(text["pass_wrong"][lang])
    return State.CHECK_PASSWORD


def start_query(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    reply_keyboard = [[text["games"][lang]], [text["random"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"][lang], reply_markup=markup)
    return State.GAMES


def rand(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    random_game = games[randint(1, 53)]["en" if lang == 1 else "ru"]
    update.message.reply_text(random_game)
    return start_query(update, context)


def ask_lang(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    reply_keyboard = [[text["langs"][0]], [text["langs"][1]]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    update.message.reply_text(text["ask_lang"][lang], reply_markup=markup)
    return State.CHOOSE_LANG


def set_lang(update: Update, context: CallbackContext):
    langs = {text["langs"][0]: 0, text["langs"][1]: 1}
    lang = langs[update.message.text]
    lang += 1  # ! need fix

    if not db_interface.check_user(update.message.chat_id):
        return ask_password(update, context)
    return start(update, context)


def stop_bot(update: Update, context: CallbackContext):
    update.message.reply_text("END")
    return ConversationHandler.END


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
