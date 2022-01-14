from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from bot.admin import admin
from bot.admin import admin_password
from bot.admin import new_password
from bot.admin import update_games
from bot.ask import ask_type
from bot.ask import final_answer
from bot.ask import read_age
from bot.ask import read_amount
from bot.ask import read_location
from bot.ask import read_props
from bot.ask import read_type
from bot.ask import result
from bot.etc import text
from bot.handlers import ask_lang
from bot.handlers import check_password
from bot.handlers import rand
from bot.handlers import set_lang
from bot.handlers import start
from bot.handlers import start_query
from bot.handlers import stop_bot
from bot.utils import State


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("admin", admin),
        CommandHandler("language", ask_lang),
    ],
    states={
        # ADMIN #
        State.ADMIN: [
            MessageHandler(Filters.text(list(text["back"].values())), start),
            MessageHandler(
                Filters.text(list(text["change_password"].values())), admin_password
            ),
            MessageHandler(Filters.text(list(text["update"].values())), update_games),
        ],
        State.ADMIN_PASSWORD: [MessageHandler(Filters.text, new_password)],
        State.CHOOSE_LANG: [
            MessageHandler(Filters.text(list(text["langs"].values())), set_lang)
        ],
        State.CHECK_PASSWORD: [MessageHandler(Filters.text, check_password)],
        # GAMES #
        State.GAMES: [
            MessageHandler(Filters.text(list(text["games"].values())), ask_type),
            MessageHandler(Filters.text(list(text["random"].values())), rand),
        ],
        # Questions #
        State.GET_TYPE: [MessageHandler(Filters.text, read_type)],
        State.GET_AGE: [MessageHandler(Filters.text, read_age)],
        State.GET_AMOUNT: [MessageHandler(Filters.text, read_amount)],
        State.GET_LOCATION: [MessageHandler(Filters.text, read_location)],
        State.GET_PROPS: [MessageHandler(Filters.text, read_props)],
        State.ANSWER: [MessageHandler(Filters.text, final_answer)],
        State.BACK_ANSWER: [
            MessageHandler(Filters.text(list(text["back"].values())), result),
            MessageHandler(Filters.text(list(text["menu"].values())), start_query),
        ],
    },
    fallbacks=[CommandHandler("stop", stop_bot)],
)
