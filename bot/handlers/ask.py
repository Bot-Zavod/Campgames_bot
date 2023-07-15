from typing import Callable
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


async def read_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_flag: int,
    question_num: int,
) -> Optional[Callable]:
    # log_message(update)
    chat_id = update.message.chat.id
    lang = get_lang(update)
    massage = update.message.text

    if massage == text["back"][lang]:
        # await start_query(update, context)
        user_manager.current_users[chat_id].take_answer(question_num - 1, None)
        return back_state
    # (massage == text["back"][lang] and user_manager.current_users[chat_id].flag == current_flag - 1)
    user_manager.current_users[chat_id].set_flag(current_flag)

    answer_id = get_answer_id(massage, lang)
    if answer_id != -1:
        user_manager.current_users[chat_id].take_answer(question_num, answer_id)
    return None


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
    return State.GET_TYPE


async def read_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    back = await read_answer(update, context, current_flag=2, question_num=0)
    if back:
        return await back(update, context)
    return await ask_age(update, context)


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    reply_keyboard = [
        [text["6-12"][lang], text["12+"][lang]],
        [text["any"][lang], text["back"][lang]],
    ]
    await send_msg_with_keyboard(update, context, text["ask_age"][lang], reply_keyboard)
    return State.GET_AGE


async def read_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    back = await read_answer(update, context, current_flag=3, question_num=1)
    if back:
        return await back(update, context, current_flag=2, question_num=0)
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
    return State.GET_AMOUNT


async def read_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    back = await read_answer(update, context, current_flag=4, question_num=2)
    if back:
        return await back(update, context, current_flag=3, question_num=1)
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
    return State.GET_LOCATION


async def read_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    back = await read_answer(update, context, current_flag=5, question_num=3)
    if back:
        return await back(update, context, current_flag=4, question_num=2)
    # ask_props
    return await ask_props(update, context)


async def back_state(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_flag: int = 6,
    question_num: int = 4,
):
    if current_flag == 6:
        return await ask_props(update, context)
    if current_flag == 5:
        return await ask_location(update, context)
    if current_flag == 4:
        return await ask_amount(update, context)
    if current_flag == 3:
        return await ask_age(update, context)
    if current_flag == 2:
        return await start_query(update, context)
    return


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
    return State.GET_PROPS


async def read_props(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message(update)
    back = await read_answer(update, context, current_flag=6, question_num=4)
    if back:
        return await back(update, context, current_flag=5, question_num=3)
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
    # and user_manager.current_users[chat_id].flag == 6
    if massage == text["back"][lang]:
        return await back_state(update, context)
        # return await start_query(update, context)
    if massage == text["menu"][lang]:
        user_manager.delete_user(chat_id)
        return await start_query(update, context)
    user_manager.current_users[chat_id].set_flag(7)

    description = db_interface.get_game_description(massage, lang)
    reply_keyboard = [[text["back"][lang], text["menu"][lang]]]
    await send_msg_with_keyboard(update, context, description, reply_keyboard)
    return State.BACK_ANSWER
