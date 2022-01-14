import os

from dotenv import load_dotenv
from loguru import logger
from telegram import Bot
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Defaults
from telegram.ext import PicklePersistence
from telegram.ext import Updater

from bot.commands import clear_bot
from bot.commands import set_bot_commands
from bot.conv_handler import conversation_handler
from bot.handlers import admin
from bot.handlers import ask_lang
from bot.handlers import check_id
from bot.handlers import check_time
from bot.handlers import error
from bot.handlers import stop_bot


logger.add(
    os.path.join("logs", "out.log"),
    rotation="1 week",
    backtrace=True,
    diagnose=True,
    serialize=True,
)
logger.debug("Modules imported succesfully")

load_dotenv()
logger.debug("Enviroment variables loaded")


def setup_bot(bot_token: str):
    """logs data about the bot"""

    bot = Bot(token=bot_token)
    logger.info(f"bot ID: {bot.id}")
    logger.info(f"bot username: {bot.username}")
    logger.info(f"bot link: {bot.link}")

    clear_bot(bot)
    set_bot_commands(bot)


def main():
    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    setup_bot(bot_token)
    main_dir = os.path.dirname(os.path.dirname(__file__))
    storage_path = os.path.join(main_dir, "storage.pickle")
    my_persistence = PicklePersistence(filename=storage_path)
    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(
        token=bot_token,
        persistence=my_persistence,
        use_context=True,
        defaults=defaults,
        workers=6,
    )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(CommandHandler("stop", stop_bot))
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("language", ask_lang))
    dispatcher.add_error_handler(error)
    # debug tools
    dispatcher.add_handler(CommandHandler("id", check_id))
    dispatcher.add_handler(CommandHandler("time", check_time))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
