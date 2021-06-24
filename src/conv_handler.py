from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from .admin import admin
from .admin import admin_password
from .admin import new_password
from .ask import ask_type
from .ask import final_answer
from .ask import read_age
from .ask import read_amount
from .ask import read_location
from .ask import read_props
from .ask import read_type
from .ask import result
from .etc import text
from .handlers import ask_lang
from .handlers import check_password
from .handlers import rand
from .handlers import set_lang
from .handlers import start
from .handlers import start_query
from .handlers import stop_bot
from .states_range import State


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("admin", admin),
        CommandHandler("language", ask_lang),
    ],
    states={
        # ADMIN #
        State.ADMIN: [
            MessageHandler(Filters.text(text["back"].values()), start),
            MessageHandler(Filters.text(text["yes"].values()), admin_password),
        ],
        State.ADMIN_PASSWORD: [MessageHandler(Filters.text, new_password)],
        State.CHOOSE_LANG: [
            MessageHandler(Filters.text(text["langs"].values()), set_lang)
        ],
        State.CHECK_PASSWORD: [MessageHandler(Filters.text, check_password)],
        # GAMES #
        State.GAMES: [
            MessageHandler(Filters.text(text["games"].values()), ask_type),
            MessageHandler(Filters.text(text["random"].values()), rand),
        ],
        # Questions #
        State.GET_TYPE: [MessageHandler(Filters.text, read_type)],
        State.GET_AGE: [MessageHandler(Filters.text, read_age)],
        State.GET_AMOUNT: [MessageHandler(Filters.text, read_amount)],
        State.GET_LOCATION: [MessageHandler(Filters.text, read_location)],
        State.GET_PROPS: [MessageHandler(Filters.text, read_props)],
        State.ANSWER: [MessageHandler(Filters.text, final_answer)],
        State.BACK_ANSWER: [
            MessageHandler(Filters.text(text["back"].values()), result),
            MessageHandler(Filters.text(text["menu"].values()), start_query),
        ],
    },
    fallbacks=[CommandHandler("stop", stop_bot)],
)
