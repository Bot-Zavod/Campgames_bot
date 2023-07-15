from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from bot.admins import ADMINS
from bot.data import text
from bot.handlers import admin
from bot.handlers import admin_password
from bot.handlers import ask_lang
from bot.handlers import ask_type
from bot.handlers import check_id
from bot.handlers import check_password
from bot.handlers import check_time
from bot.handlers import final_answer
from bot.handlers import new_password
from bot.handlers import rand
from bot.handlers import read_age
from bot.handlers import read_amount
from bot.handlers import read_location
from bot.handlers import read_props
from bot.handlers import read_type
from bot.handlers import result
from bot.handlers import set_lang
from bot.handlers import start
from bot.handlers import start_query
from bot.handlers import stop_bot
from bot.handlers import update_games
from bot.utils import State

admin_filters = filters.User(ADMINS) & filters.ChatType.PRIVATE

commands = [
    CommandHandler("language", ask_lang),
    CommandHandler("id", check_id),
    CommandHandler("time", check_time),
]

# back_keys = keys = list(text["back"].values())
# any_keys = keys = list(text["any"].values())


# def list_keyboard(key: str) -> List[str]:
#     keys = list(text[key].values())
#     keys += back_keys
#     keys += any_keys
#     return keys


conversation_handler = ConversationHandler(
    name="base_conversation",
    entry_points=[CommandHandler("start", start)],
    states={
        ##################
        # GAMES ##########
        ##################
        State.GAMES: [
            MessageHandler(filters.Text(list(text["games"].values())), ask_type),
            MessageHandler(filters.Text(list(text["random"].values())), rand),
            CommandHandler("language", ask_lang),
        ],
        ##################
        # Questions ######
        ##################
        State.CHECK_PASSWORD: [MessageHandler(filters.TEXT, check_password)],
        State.CHOOSE_LANG: [
            MessageHandler(filters.Text(list(text["langs"].values())), set_lang)
        ],
        State.GET_TYPE: [MessageHandler(filters.TEXT, read_type)],
        State.GET_AGE: [MessageHandler(filters.TEXT, read_age)],
        State.GET_AMOUNT: [MessageHandler(filters.TEXT, read_amount)],
        State.GET_LOCATION: [MessageHandler(filters.TEXT, read_location)],
        State.GET_PROPS: [MessageHandler(filters.TEXT, read_props)],
        State.ANSWER: [MessageHandler(filters.TEXT, final_answer)],
        State.BACK_ANSWER: [
            MessageHandler(filters.Text(list(text["back"].values())), result),
            MessageHandler(filters.Text(list(text["menu"].values())), start_query),
        ],
    },
    fallbacks=[CommandHandler("stop", stop_bot)],
)

admin_handler = ConversationHandler(
    name="admin_conversation",
    persistent=True,
    allow_reentry=True,
    entry_points=[CommandHandler("admin", admin, filters=admin_filters)],
    states={
        # -----------------------------------------------------------
        # Admin
        # -----------------------------------------------------------
        State.ADMIN: [
            MessageHandler(
                filters.Text(list(text["change_password"].values())), admin_password
            ),
            MessageHandler(filters.Text(list(text["update"].values())), update_games),
        ],
        State.ADMIN_PASSWORD: [MessageHandler(filters.TEXT, new_password)],
        State.CHOOSE_LANG: [
            MessageHandler(filters.Text(list(text["langs"].values())), set_lang)
        ],
        State.CHECK_PASSWORD: [MessageHandler(filters.TEXT, check_password)],
    },
    fallbacks=[CommandHandler("stop", stop_bot)],
)
