from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from bot.data import text
from bot.utils import State

# from bot.utils import get_lang


async def start_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # lang = get_lang(update)
    """reply_keyboard = [
        [text["games"][lang]],
        [text["random"][lang]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=text["start_games"][lang], reply_markup=markup
    )"""

    reply_keyboard = [
        [text["games"]],
        [text["random"]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    chat_id = update.message.chat.id
    await context.bot.send_message(
        chat_id=chat_id, text=text["start_games"], reply_markup=markup
    )
    return State.GAMES

def change_indent(description:str):
    if description.find('\n')==-1:
        return description
    index = description.find("\n")
    text_str = ''
    if description[index+1]!='\n':
        text_str = '\n'
    if description[index+2]=='\n':
        description = description.replace('\n','',1)
        index+=1
    description = f"<b>{description[:index]}</b>" + text_str + description[index:]
    return description