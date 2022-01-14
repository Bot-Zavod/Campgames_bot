from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from bot.database import db_interface
from bot.etc import text
from bot.utils import logger
from bot.utils import State


def start(update: Update, context: CallbackContext):
    """check if user is authorized and have language"""
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)

    if lang is None:
        return ask_lang(update, context)
    if not db_interface.check_user(chat_id):
        return ask_password(update, context)

    update.message.reply_text(text["start"][lang], reply_markup=ReplyKeyboardRemove())
    return start_query(update, context)


def ask_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    update.message.reply_text(
        text["ask_pass"][lang], reply_markup=ReplyKeyboardRemove()
    )
    return State.CHECK_PASSWORD


def check_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = db_interface.get_language(chat_id)
    with open("password.txt", "r") as file:
        password = file.readline().strip()

    if update.message.text == password:
        db_interface.authorize_user(chat_id)
        update.message.reply_text(text["pass_success"][lang])
        return start_query(update, context)

    update.message.reply_text(text["pass_wrong"][lang])
    return State.CHECK_PASSWORD


def start_query(update: Update, context: CallbackContext):
    lang = db_interface.get_language(update.message.chat.id)
    reply_keyboard = [[text["games"][lang]], [text["random"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"][lang], reply_markup=markup)
    return State.GAMES


def rand(update: Update, context: CallbackContext):
    lang = db_interface.get_language(update.message.chat.id)
    random_game = db_interface.get_random_game_description(lang)
    update.message.reply_text(random_game)


def ask_lang(update: Update, context: CallbackContext):
    reply_keyboard = [[text["langs"][0]], [text["langs"][1]]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    lang = db_interface.get_language(update.message.chat.id)
    update.message.reply_text(text["ask_lang"][lang], reply_markup=markup)
    return State.CHOOSE_LANG


def set_lang(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    langs = {text["langs"][0]: 0, text["langs"][1]: 1}
    lang = langs.get(update.message.text, None)
    if lang is None:
        return ask_lang(update, context)
    db_interface.set_language(chat_id, lang)

    if not db_interface.check_user(chat_id):
        return ask_password(update, context)
    return start(update, context)


def stop_bot(update: Update, context: CallbackContext):
    update.message.reply_text("END")
    return ConversationHandler.END


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
