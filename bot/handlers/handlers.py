import html
import json
import os
import sys
import traceback
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


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer"""
    # we want to notify the user of this problem.
    # This will always work, but not notify users if the update is an
    # callback or inline query, or a poll update.
    # In case you want this, keep in mind that sending the message could fail

    if update:
        local_upd = (
            update.effective_message if update.effective_message else update.message
        )
    else:
        local_upd = None

    chat_id = None
    if local_upd:
        chat_id = local_upd.chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text=text["server_error"][1],
        )

    # Log the error before we do anything else, so we can see it even if something breaks.

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    error_tb = "".join(tb_list)
    logger.bind(chat_id=chat_id).error(f"Exception while handling an update:{error_tb}")
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    bot_username = "@" + context.bot.username + "\n\n"
    if update:
        update_json = json.dumps(update.to_dict(), indent=2, ensure_ascii=False)
    else:
        update_json = ""
    error_message = (
        "{}"
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>context.chat_data = {}</pre>\n\n"
        "<pre>context.user_data = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        bot_username,
        html.escape(update_json),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(error_tb),
    )

    # Finally, send the message
    log_channel = "@" + os.environ["LOG_CHANNEL"]

    # dont print to debug channel in case that's not a production server
    if ("--debug" not in sys.argv) and ("-d" not in sys.argv):
        if len(error_message) < 4096:
            context.bot.send_message(chat_id=log_channel, text=error_message)
        else:
            msg_parts = len(error_message) // 4080
            for i in range(msg_parts):
                err_msg_truncated = error_message[i : i + 4080]
                if i == 0:
                    error_message_text = err_msg_truncated + "</pre>"
                elif i < msg_parts:
                    error_message_text = "<pre>" + err_msg_truncated + "</pre>"
                else:
                    error_message_text = "<pre>" + err_msg_truncated
                context.bot.send_message(chat_id=log_channel, text=error_message_text)
