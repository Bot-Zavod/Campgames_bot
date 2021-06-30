from typing import Callable
from typing import Dict
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext

from .database import db_interface
from .etc import text
from .handlers import start_query
from .states_range import State
from .user_manager import User
from .user_manager import user_manager
from .utils import get_language
from .utils import send_msg_with_keyboard


def get_answer_id(msg: str, lang: int) -> int:
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
    return choices.get(msg, -1)


def read_answer(
    update: Update, context: CallbackContext, current_flag: int, question_num: int
) -> Optional[Callable]:
    lang = get_language(update, context)
    chat_id = update.message.chat.id
    massage = update.message.text

    if (
        massage == text["back"][lang]
        and user_manager.current_users[chat_id].flag == current_flag - 1
    ):
        return start_query
    user_manager.current_users[chat_id].set_flag(current_flag)

    answer_id = get_answer_id(massage, lang)
    if answer_id != -1:
        user_manager.current_users[chat_id].take_answer(question_num, answer_id)
    return None


def ask_type(update: Update, context: CallbackContext):
    user_manager.create_user(User(update.message.chat.id, update.message.chat.username))
    lang = get_language(update, context)

    user_manager.current_users[update.message.chat.id].set_flag(1)
    reply_keyboard = [
        [text["team_building"][lang]],
        [text["ice_breaker"][lang]],
        [text["timefiller"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    send_msg_with_keyboard(update, text["ask_type"][lang], reply_keyboard)
    return State.GET_TYPE


def read_type(update: Update, context: CallbackContext):
    back = read_answer(update, context, current_flag=2, question_num=0)
    if back:
        return back(update, context)
    return ask_age(update, context)


def ask_age(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    reply_keyboard = [
        [text["6-12"][lang], text["12+"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    send_msg_with_keyboard(update, text["ask_age"][lang], reply_keyboard)
    return State.GET_AGE


def read_age(update: Update, context: CallbackContext):
    back = read_answer(update, context, current_flag=3, question_num=1)
    if back:
        return back(update, context)
    return ask_amount(update, context)


def ask_amount(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    reply_keyboard = [
        [text["up to 5"][lang], text["5-20"][lang], text["20+"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    send_msg_with_keyboard(update, text["ask_amount"][lang], reply_keyboard)
    return State.GET_AMOUNT


def read_amount(update: Update, context: CallbackContext):
    back = read_answer(update, context, current_flag=4, question_num=2)
    if back:
        return back(update, context)
    return ask_location(update, context)


def ask_location(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    reply_keyboard = [
        [text["outside"][lang], text["inside"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    send_msg_with_keyboard(update, text["ask_location"][lang], reply_keyboard)
    return State.GET_LOCATION


def read_location(update: Update, context: CallbackContext):
    back = read_answer(update, context, current_flag=5, question_num=3)
    if back:
        return back(update, context)
    return ask_props(update, context)


def ask_props(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    reply_keyboard = [
        [text["yes"][lang], text["no"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    send_msg_with_keyboard(update, text["ask_props"][lang], reply_keyboard)
    return State.GET_PROPS


def read_props(update: Update, context: CallbackContext):
    back = read_answer(update, context, current_flag=6, question_num=4)
    if back:
        return back(update, context)
    return result(update, context)


def result(update: Update, context: CallbackContext):
    lang = get_language(update, context)
    answers = user_manager.current_users[update.message.chat.id].answers
    games = db_interface.get_game_names(*answers)

    reply_keyboard = [[game_name[lang + 1]] for game_name in games]
    reply_keyboard.append([text["back"][lang], text["menu"][lang]])
    send_msg_with_keyboard(update, text["answer"][lang], reply_keyboard)
    return State.ANSWER


def final_answer(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = get_language(update, context)
    massage = update.message.text
    if massage == text["back"][lang] and user_manager.current_users[chat_id].flag == 6:
        return ask_props(update, context)
    if massage == text["menu"][lang]:
        user_manager.delete_user(chat_id)
        return start_query(update, context)
    user_manager.current_users[chat_id].set_flag(7)

    description = db_interface.get_game_description(massage, lang)
    reply_keyboard = [[text["back"][lang], text["menu"][lang]]]
    send_msg_with_keyboard(update, description, reply_keyboard)
    return State.BACK_ANSWER
