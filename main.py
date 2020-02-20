from etc import text, games, names
from os import getcwd, environ
import init
import logging
from random import randint
from database import DbInterface
from user import UserManager, User
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

init.init()

# link = getcwd().split("\\")
# link = link[:-1]
# link = "\\\\".join(link)+"\\\\database.db"
# print(r"{}".format(link))
# db = DbInterface(r"{}".format(link))
# # C:\\Users\\Илон Маск\\Dropbox\\Programming_projects\\database.db
db = DbInterface(r"D:\Dropbox\\Programming_projects\\Campgames_bot\\database.db")
print(db)
CHOOSE_LANG, CHECK_PASSWORD, ADMIN, GAMES, BACK, ASK_TYPE, ASK_AGE, ASK_AMOUNT, ASK_LOCATION, ASK_PROPS, RESULT, ANSWER,BACK_ANSWER = range(13)

UM = UserManager()

def language(update,context):
    lang = db.getLang(update.message.chat_id)
    if lang == None:
        lang = 1
    return lang

def start_query(update, context):
    lang = language(update,context)
    reply_keyboard = [[text["games"][lang]],[text["random"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"][lang], reply_markup = markup)
    return GAMES

def game_start(update,context):
    lang = language(update,context)
    if update.message.text == text["games"][lang]:
        return a_type(update,context)
    elif update.message.text == text["random"][lang]:
        return rand(update,context)

def rand(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    reply_keyboard = [[text["back"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(games[randint(1,53)]["en" if lang==1 else "ru"], reply_markup = markup)
    return BACK

def back(update,context):
    lang = language(update,context)
    if update.message.text == text["back"][lang]:
        return start_query(update, context)
        

def a_type(update,context):
    UM.create_user(User(update.message.chat.id,update.message.chat.username))
    lang = UM.currentUsers[update.message.chat.id].lang

    UM.currentUsers[update.message.chat.id].set_flag(1)
    reply_keyboard = [[text["team_building"][lang]],[text["ice_breaker"][lang]],[text["timefiller"][lang]],
                      [text["any"][lang],text["back"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_type"][lang], reply_markup = markup)
    return ASK_AGE

def a_age(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    massage = update.message.text
    if massage == text["team_building"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(0,0)
    elif massage == text["ice_breaker"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(0,1)
    elif massage == text["timefiller"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(0,2)
    elif massage == text["back"][lang] and UM.currentUsers[update.message.chat.id].flag == 1:
        return start_query(update,context)
    elif massage == text["any"][lang]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(2)

    reply_keyboard = [[text["6-12"],text["12+"]],
                      [text["any"][lang],text["back"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_age"][lang], reply_markup = markup)
    return ASK_AMOUNT

def a_amount(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    massage = update.message.text
    if massage == text["6-12"]:
        UM.currentUsers[update.message.chat.id].take_answer(1,0)
    elif massage == text["12+"]:
        UM.currentUsers[update.message.chat.id].take_answer(1,1)
    elif massage == text["back"][lang] and UM.currentUsers[update.message.chat.id].flag == 2:
        return a_type(update,context)
    elif massage == text["any"][lang]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(3)

    reply_keyboard = [[text["up to 5"][lang],text["5-20"],text["20+"]],
                      [text["any"][lang],text["back"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_amount"][lang], reply_markup = markup)
    return ASK_LOCATION

def a_location(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    massage = update.message.text
    if massage == text["up to 5"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(2,0)
    elif massage == text["5-20"]:
        UM.currentUsers[update.message.chat.id].take_answer(2,1)
    elif massage == text["20+"]:
        UM.currentUsers[update.message.chat.id].take_answer(2,2)
    elif massage == text["back"][lang] and UM.currentUsers[update.message.chat.id].flag == 3:
        return a_age(update,context)
    elif massage == text["any"][lang]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(4)

    reply_keyboard = [[text["outside"][lang],text["inside"][lang]],
                      [text["any"][lang],text["back"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_location"][lang], reply_markup = markup)
    return ASK_PROPS

def a_props(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    massage = update.message.text
    if massage == text["outside"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(3,0)
    elif massage == text["inside"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(3,1)
    elif massage == text["back"][lang] and UM.currentUsers[update.message.chat.id].flag == 4:
        return a_amount(update,context)
    elif massage == text["any"][lang]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(5)

    reply_keyboard = [[text["yes"][lang],text["no"][lang]],
                      [text["any"][lang],text["back"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_props"][lang], reply_markup = markup)
    return RESULT

def result(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    massage = update.message.text
    if massage == text["no"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(4,0)
    elif massage == text["yes"][lang]:
        UM.currentUsers[update.message.chat.id].take_answer(4,1)
    elif massage == text["back"][lang] and UM.currentUsers[update.message.chat.id].flag == 5:
        return a_location(update,context)
    elif massage == text["any"][lang]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(6)

    answer = UM.currentUsers[update.message.chat.id].answers
    update.message.reply_text(answer)
    game_id = db.getGames(answer[0],answer[1],answer[2],answer[3],answer[4])
    buttons_language = "en" if lang==1 else "ru"
    reply_keyboard = [[names[i][buttons_language]] for i in game_id]
    reply_keyboard.append([text["back"][lang],text["menu"][lang]])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["answer"][lang], reply_markup = markup)
    return ANSWER

def final_answer(update,context):
    lang = UM.currentUsers[update.message.chat.id].lang
    massage = update.message.text
    if massage == text["back"][lang] and UM.currentUsers[update.message.chat.id].flag == 6:
        return a_props(update,context)
    elif massage == text["menu"][lang]:
        UM.delete_user(update.message.chat.id)
        return start_query(update, context)
    UM.currentUsers[update.message.chat.id].set_flag(7)

    solution = None
    language = "en" if lang==1 else "ru"
    for key in names:
        if massage == names[key][language]:
            solution = key
            break
    reply_keyboard = [[text["back"][lang],text["menu"][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(games[solution][language], reply_markup = markup)
    return BACK_ANSWER

def back_answer(update,context):
    massage = update.message.text
    lang = UM.currentUsers[update.message.chat.id].lang
    if massage == text["back"][lang]:
        return result(update,context)
    elif massage == text["menu"][lang]:
        return start_query(update, context)


def start(update, context):
    lang = language(update,context)

    update.message.reply_text(text["start"][lang], reply_markup = ReplyKeyboardRemove())
    db_lang = db.getLang(update.message.chat_id)
    if db_lang is None:
        return ask_lang(update, context)
    if not db.checkUser(update.message.chat_id):
        return ask_password(update, context)
    return start_query(update, context)

def ask_password(update, context):
    lang = language(update,context)
    update.message.reply_text(text["ask_pass"][lang])
    return CHECK_PASSWORD

def check_password(update, context):
    lang = language(update,context)
    FILENAME = r"password.txt"
    with open(FILENAME, "r") as file:
        PASSWORD = file.readline()
        file.close()
    if update.message.text == PASSWORD:
        db.authorizeUser(update.message.chat_id)
        update.message.reply_text(text["pass_success"][lang])
        return start_query(update, context)
    else:
        update.message.reply_text(text["pass_wrong"][lang])
        return CHECK_PASSWORD

def ask_lang(update, context):
    lang = language(update,context)
    reply_keyboard = [[text["ru"]],[text["en"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(text["ask_lang"][lang], reply_markup = markup)
    return CHOOSE_LANG

def set_lang(update, context):
    lang = None
    if update.message.text == text["ru"]:
        lang = 0
    elif update.message.text == text["en"]:
        lang = 1
    if lang == 0 or lang == 1:
        db.setLang(update.message.chat_id, lang)
    else:
        update.message.reply_text(text["unknown"][lang])
        return CHOOSE_LANG
    if not db.checkUser(update.message.chat_id):
        return ask_password(update, context)
    return start(update, context)

def admin(update, context):
    lang = language(update,context)
    if update.message.chat.username in ("V_vargan","lisatkachenko"):
        FILENAME = r"password.txt"
        with open(FILENAME, "r") as file:
            PASSWORD = file.readline()
            file.close()
        update.message.reply_text("Hi boss, current password is\n\n"+PASSWORD)
        reply_keyboard = [[text["yes"][lang],text["back"][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Would you like to change it?", reply_markup = markup)
        return ADMIN
    else:
        update.message.reply_text("You are not my boss, maybe later)")
        return start(update, context)

def admin_password(update, context):
    lang = language(update,context)
    if update.message.text == text["back"][lang]:
        return start(update, context)
    elif update.message.text == text["yes"][lang]:
        update.message.reply_text("Ok man, set the new PASSWORD")

def done(update, context):

    update.message.reply_text('END')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(environ['bot_token'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSE_LANG, ASK_AGE, ASK_AMOUNT, ASK_LOCATION, ASK_PROPSand START_QUERY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('admin', admin)],

        states={
            ADMIN: [MessageHandler(Filters.text, admin_password)],
            CHOOSE_LANG: [MessageHandler(Filters.text, set_lang)],
            CHECK_PASSWORD: [MessageHandler(Filters.text, check_password)],
            GAMES: [MessageHandler(Filters.text, game_start)],
            BACK: [MessageHandler(Filters.text, back)],
            ASK_TYPE: [MessageHandler(Filters.text, a_type)],
            ASK_AGE: [MessageHandler(Filters.text, a_age)],
            ASK_AMOUNT: [MessageHandler(Filters.text, a_amount)],
            ASK_LOCATION: [MessageHandler(Filters.text, a_location)],
            ASK_PROPS: [MessageHandler(Filters.text, a_props)],
            RESULT: [MessageHandler(Filters.text, result)],
            ANSWER: [MessageHandler(Filters.text, final_answer)],
            BACK_ANSWER: [MessageHandler(Filters.text, back_answer)],
        },

        fallbacks=[CommandHandler('stop', done),]
                #    CommandHandler('start', start),
                #    CommandHandler('admin', admin),
                #    CommandHandler('language', ask_lang)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()