from typing import Callable

from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from bot.admins import ADMINS
from bot.data import text
from bot.handlers import admin
from bot.handlers import admin_password
from bot.handlers import ask
from bot.handlers import check_id
from bot.handlers import check_password
from bot.handlers import check_time
from bot.handlers import new_password
from bot.handlers import rand
from bot.handlers import start
from bot.handlers import start_query
from bot.handlers import stop_bot
from bot.handlers import update_games
from bot.utils import State

# from bot.handlers import ask_lang
# from bot.handlers import set_lang

admin_filters = filters.User(ADMINS) & filters.ChatType.PRIVATE

commands = [
    # CommandHandler("language", ask_lang),
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


def back_handler(callback: Callable) -> MessageHandler:
    #return MessageHandler(filters.Text(list(text["back"].values())), callback)
    return MessageHandler(filters.Text(text["back"]), callback)


conversation_handler = ConversationHandler(
    name="base_conversation",
    entry_points=[CommandHandler("start", start)],
    states={
        ##################
        # GAMES ##########
        ##################
        State.GAMES: [
            MessageHandler(filters.Text(text["games"]), ask.ask_type),
            MessageHandler(filters.Text(text["random"]), rand),
            # MessageHandler(filters.Text(list(text["games"].values())), ask.ask_type),
            # MessageHandler(filters.Text(list(text["random"].values())), rand),
            # MessageHandler(filters.Text(list(text["ask_lang"].values())), ask_lang),
            # CommandHandler("language", ask_lang),
        ],
        ##################
        # Questions ######
        ##################
        State.CHECK_PASSWORD: [MessageHandler(filters.TEXT, check_password)],
        # State.CHOOSE_LANG: [MessageHandler(filters.Text(list(text["langs"].values())), set_lang)],
        State.READ_TYPE: [
            back_handler(start_query),
            MessageHandler(filters.TEXT, ask.read_type),
        ],
        State.READ_AGE: [
            back_handler(ask.ask_type),
            MessageHandler(filters.TEXT, ask.read_age),
        ],
        State.READ_AMOUNT: [
            back_handler(ask.ask_age),
            MessageHandler(filters.TEXT, ask.read_amount),
        ],
        State.READ_LOCATION: [
            back_handler(ask.ask_amount),
            MessageHandler(filters.TEXT, ask.read_location),
        ],
        State.READ_PROPS: [
            back_handler(ask.ask_location),
            MessageHandler(filters.TEXT, ask.read_props),
        ],
        State.ANSWER: [
            back_handler(ask.ask_props),
            MessageHandler(filters.TEXT, ask.final_answer),
        ],
        State.BACK_ANSWER: [
            back_handler(ask.result),
            #MessageHandler(filters.Text(list(text["menu"].values())), start_query),
            MessageHandler(filters.Text(text["menu"]), start_query),
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
                #filters.Text(list(text["change_password"].values())), admin_password
                filters.Text(text["change_password"]), admin_password
            ),
            #MessageHandler(filters.Text(list(text["update"].values())), update_games),
            MessageHandler(filters.Text(text["update"]), update_games),
        ],
        State.ADMIN_PASSWORD: [MessageHandler(filters.TEXT, new_password)],
        # State.CHOOSE_LANG: [MessageHandler(filters.Text(list(text["langs"].values())), set_lang)],
        State.CHECK_PASSWORD: [MessageHandler(filters.TEXT, check_password)],
    },
    fallbacks=[CommandHandler("stop", stop_bot)],
)
