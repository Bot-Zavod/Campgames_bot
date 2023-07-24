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

admin_filters = filters.User(ADMINS) & filters.ChatType.PRIVATE

commands = [
    CommandHandler("id", check_id),
    CommandHandler("time", check_time),
]


def back_handler(callback: Callable) -> MessageHandler:
    return MessageHandler(filters.Text([text["back"]]), callback)


conversation_handler = ConversationHandler(
    name="base_conversation",
    entry_points=[CommandHandler("start", start)],
    states={
        ##################
        # GAMES ##########
        ##################
        State.GAMES: [  # TODO: filters.Text takes a list of strings, not a single string
            MessageHandler(filters.Text([text["games"]]), ask.ask_type),
            MessageHandler(filters.Text([text["random"]]), rand),
        ],
        ##################
        # Questions ######
        ##################
        State.CHECK_PASSWORD: [MessageHandler(filters.TEXT, check_password)],
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
            MessageHandler(filters.Text([text["menu"]]), start_query),
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
                filters.Text([text["change_password"]]),
                admin_password,
            ),
            MessageHandler(filters.Text([text["update"]]), update_games),
        ],
        State.ADMIN_PASSWORD: [MessageHandler(filters.TEXT, new_password)],
        State.CHECK_PASSWORD: [MessageHandler(filters.TEXT, check_password)],
    },
    fallbacks=[CommandHandler("stop", stop_bot)],
)
