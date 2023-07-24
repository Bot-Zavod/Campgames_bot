from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes


async def send_msg_with_keyboard(
    update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str, reply_keyboard: list
):
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=msg, reply_markup=markup, parse_mode="HTML"
    )
