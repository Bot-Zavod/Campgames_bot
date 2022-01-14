from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

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


commands = [
    CommandHandler("start", start),
    CommandHandler("stop", stop_bot),
    CommandHandler("admin", admin),
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


states = {
    ##################
    # ADMIN #########
    ##################
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
    ##################
    # GAMES ##########
    ##################
    State.GAMES: [
        MessageHandler(Filters.text(list(text["games"].values())), ask_type),
        MessageHandler(Filters.text(list(text["random"].values())), rand),
    ],
    ##################
    # Questions ######
    ##################
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
}


for key, value in states.items():
    states[key] = commands + value


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states=states,
    fallbacks=[CommandHandler("stop", stop_bot)],
)
