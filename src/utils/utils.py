from telegram import ReplyKeyboardMarkup
from telegram import Update


def send_msg_with_keyboard(update: Update, msg: str, reply_keyboard: list):
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(msg, reply_markup=markup)
