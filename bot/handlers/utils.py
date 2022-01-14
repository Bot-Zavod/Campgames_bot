from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from bot.data import text
from bot.utils import get_lang
from bot.utils import State


def start_query(update: Update, context: CallbackContext):
    lang = get_lang(update)
    reply_keyboard = [[text["games"][lang]], [text["random"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"][lang], reply_markup=markup)
    return State.GAMES
