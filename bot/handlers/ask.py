from typing import Dict
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from bot.data import text
from bot.database import db_interface
from bot.handlers.utils import start_query
from bot.utils import get_lang
from bot.utils import send_msg_with_keyboard
from bot.utils import State
from bot.utils import User
from bot.utils import user_manager
from bot.utils.logs import log_message


class QuestionType:
    type_ = 0
    age = 1
    amount = 2
    location = 3
    props = 4


def get_answer_id(msg: str, lang: int) -> Optional[int]:
    # always return -1 if msg is not in choices
    choices: Dict[str, int] = {
        # type
        text["team_building"][lang]: 0,
        text["ice_breaker"][lang]: 1,
        text["timefiller"][lang]: 2,
        # age
        text["6-12"][lang]: 0,
        text["12+"][lang]: 1,
        # count
        text["up to 5"][lang]: 0,
        text["5-20"][lang]: 1,
        text["20+"][lang]: 2,
        # place
        text["outside"][lang]: 0,
        text["inside"][lang]: 1,
        # props
        text["no"][lang]: 0,
        text["yes"][lang]: 1,
    }
    return choices.get(msg)


async def read_answer(update: Update, question_num: int):
    chat_id = update.message.chat.id
    lang = get_lang(update)

    answer_id = get_answer_id(update.message.text, lang)
    user_manager.take_answer(chat_id, question_num, answer_id)
    # TODO user_manager.take_answer(chat_id, question_num, answer_id)(completed)
    # TODO question_num -> Enum with questions (type, age, count, place, props)(completed)


async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    lang = get_lang(update)
    user_manager.create_user(User(chat_id, update.message.chat.username))

    user_manager.current_users[chat_id].set_flag(1)
    reply_keyboard = [
        [text["team_building"][lang]],
        [text["ice_breaker"][lang]],
        [text["timefiller"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    await send_msg_with_keyboard(
        update, context, text["ask_type"][lang], reply_keyboard
    )
    return State.READ_TYPE


async def read_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    await read_answer(update, question_num=QuestionType.type_)
    return await ask_age(update, context)


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    reply_keyboard = [
        [text["6-12"][lang], text["12+"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    await send_msg_with_keyboard(update, context, text["ask_age"][lang], reply_keyboard)
    return State.READ_AGE


async def read_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    await read_answer(update, question_num=QuestionType.age)
    return await ask_amount(update, context)


async def ask_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    reply_keyboard = [
        [text["up to 5"][lang], text["5-20"][lang], text["20+"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    await send_msg_with_keyboard(
        update, context, text["ask_amount"][lang], reply_keyboard
    )
    return State.READ_AMOUNT


async def read_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    await read_answer(update, question_num=QuestionType.amount)
    return await ask_location(update, context)


async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    reply_keyboard = [
        [text["outside"][lang], text["inside"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    await send_msg_with_keyboard(
        update, context, text["ask_location"][lang], reply_keyboard
    )
    return State.READ_LOCATION


async def read_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    await read_answer(update, question_num=QuestionType.location)
    return await ask_props(update, context)


async def ask_props(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    lang = get_lang(update)
    reply_keyboard = [
        [text["yes"][lang], text["no"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    await send_msg_with_keyboard(
        update, context, text["ask_props"][lang], reply_keyboard
    )
    return State.READ_PROPS


async def read_props(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    await read_answer(update, question_num=QuestionType.props)
    return await result(update, context)


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    lang = get_lang(update)
    answers = user_manager.current_users[chat_id].answers
    games = db_interface.get_game_names(*answers)

    reply_keyboard = [[game_name[lang + 1]] for game_name in games]
    reply_keyboard.append([text["back"][lang], text["menu"][lang]])
    await send_msg_with_keyboard(update, context, text["answer"][lang], reply_keyboard)
    return State.ANSWER


async def final_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    chat_id = update.message.chat.id
    lang = get_lang(update)
    massage = update.message.text

    if massage == text["menu"][lang]:
        user_manager.delete_user(chat_id)
        return await start_query(update, context)
    user_manager.current_users[chat_id].set_flag(7)

    description = db_interface.get_game_description(massage, lang)
    reply_keyboard = [[text["back"][lang], text["menu"][lang]]]
    await send_msg_with_keyboard(update, context, description, reply_keyboard)
    return State.BACK_ANSWER
