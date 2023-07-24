from functools import wraps

from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from bot.admins import ADMINS
from bot.config import settings
from bot.data import text
from bot.password import get_password
from bot.password import write_password
from bot.utils import State
from bot.utils import update_games_in_db
from bot.utils.logs import log_message

# from bot.handlers.handlers import set_lang
# from bot.utils import get_lang


GAMES_TABLE_KEY = settings.GAMES_TABLE_KEY


def restrict_user(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.id in ADMINS:
            return await func(update, context)
        # lang = get_lang(update)
        chat_id = update.message.chat.id
        # await context.bot.send_message(chat_id=chat_id, text=text["sorry"][lang])
        await context.bot.send_message(chat_id=chat_id, text=text["sorry"])
        return None

    return wrapper


@restrict_user
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)

    password = get_password()
    reply_keyboard = [
        [text["update"]],
        [text["change_password"]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=text["hi_boss"] + password, reply_markup=markup
    )
    return State.ADMIN


@restrict_user
async def update_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    msg_text = ""
    try:
        num_rows_deleted, games = update_games_in_db()
        msg_text += f"Deleted {num_rows_deleted} rows\nAdded {games} rows\nFrom table: https://docs.google.com/spreadsheets/d/{GAMES_TABLE_KEY}/"
    except Exception as error:
        msg_text += "Failed with " + str(error)
    chat_id = update.message.chat.id
    await context.bot.send_message(chat_id=chat_id, text=msg_text)


@restrict_user
async def admin_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    # lang = get_lang(update)
    chat_id = update.message.chat.id
    # await context.bot.send_message(chat_id=chat_id, text=text["send_pass"][lang])
    await context.bot.send_message(chat_id=chat_id, text=text["send_pass"])
    return State.ADMIN_PASSWORD


@restrict_user
async def new_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    # lang = get_lang(update)
    write_password(update.message.text)
    chat_id = update.message.chat.id
    # await context.bot.send_message(chat_id=chat_id, text=text["new_pass"][lang] + update.message.text)
    await context.bot.send_message(
        chat_id=chat_id, text=text["new_pass"] + update.message.text
    )
    return await admin(update, context)
