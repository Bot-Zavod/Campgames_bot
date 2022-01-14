from datetime import datetime

from loguru import logger
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from bot.data import text
from bot.database import db_interface
from bot.handlers.utils import start_query
from bot.password import validate_password
from bot.utils import State
from bot.utils.logs import log_message


def start(update: Update, context: CallbackContext):
    """check if user is authorized and have language"""

    log_message(update)
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)

    if lang is None:
        return ask_lang(update, context)
    if not db_interface.check_user(chat_id):
        return ask_password(update, context)

    update.message.reply_text(text["start"][lang], reply_markup=ReplyKeyboardRemove())
    return start_query(update, context)


def rand(update: Update, context: CallbackContext):
    log_message(update)
    lang = db_interface.get_language(update.message.chat.id)
    random_game = db_interface.get_random_game_description(lang)
    update.message.reply_text(random_game)


def stop_bot(update: Update, context: CallbackContext):
    log_message(update)
    update.message.reply_text("END")
    return ConversationHandler.END


################################
###### Language ################
################################


def ask_lang(update: Update, context: CallbackContext):
    log_message(update)
    reply_keyboard = [[text["langs"][0]], [text["langs"][1]]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    lang = db_interface.get_language(update.message.chat.id)
    ask_text = ""
    if lang:
        ask_text += text["ask_lang"][lang]
    else:
        ask_text += text["ask_lang"][0] + "\n" + text["ask_lang"][1]
    update.message.reply_text(ask_text, reply_markup=markup)
    return State.CHOOSE_LANG


def set_lang(update: Update, context: CallbackContext):
    log_message(update)
    chat_id = update.message.chat.id

    langs = {text["langs"][0]: 0, text["langs"][1]: 1}
    lang = langs.get(update.message.text, None)
    if lang is None:
        return ask_lang(update, context)
    db_interface.set_language(chat_id, lang)

    if not db_interface.check_user(chat_id):
        return ask_password(update, context)
    return start(update, context)


################################
###### Password ################
################################


def ask_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    update.message.reply_text(
        text["ask_pass"][lang], reply_markup=ReplyKeyboardRemove()
    )
    return State.CHECK_PASSWORD


def check_password(update: Update, context: CallbackContext):
    log_message(update)
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)

    if validate_password(update.message.text):
        db_interface.authorize_user(chat_id)
        update.message.reply_text(text["pass_success"][lang])
        return start_query(update, context)

    update.message.reply_text(text["pass_wrong"][lang])
    return State.CHECK_PASSWORD


################################
###### UTILS ################
################################


def check_id(update: Update, context: CallbackContext):
    """return user id"""

    log_message(update)
    chat_id = update.message.chat.id
    update.message.reply_text(text=f"chat_id: {chat_id}")


def check_time(update: Update, context: CallbackContext):
    """return current server time"""

    log_message(update)
    kiev_now = datetime.now()
    update.message.reply_text(
        f"Current server time\n{str(kiev_now)}",
    )


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    log_message(update)
    logger.warning(f'Update "{update}" caused error "{context.error}"')
