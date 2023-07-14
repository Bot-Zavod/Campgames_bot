from loguru import logger
from telegram.constants import ParseMode
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import Defaults
from telegram.ext import PicklePersistence

from bot.commands import clear_bot
from bot.commands import set_bot_commands
from bot.config import settings
from bot.conv_handler import admin_handler
from bot.conv_handler import conversation_handler
from bot.handlers import check_id
from bot.handlers import check_time
from bot.handlers import error_handler

# from bot.handlers import ask_lang


logger.add(
    settings.APP_DIR / "logs" / "out.log",
    rotation="49 MB",
    backtrace=True,
    diagnose=True,
    serialize=True,
)
logger.debug(f"Вase_folder: {settings.APP_DIR}")

logger.debug("Modules imported succesfully")


async def setup_bot(application: Application):
    """logs data about the bot"""

    bot = application.bot
    logger.info(f"bot ID: {bot.id}")
    logger.info(f"bot username: {bot.username}")
    logger.info(f"bot link: {bot.link}")

    await clear_bot(bot)
    await set_bot_commands(bot)


def run_bot():
    """Inicialise handlers and start the bot"""

    builder = Application.builder()

    # TOKEN
    builder.token(settings.BOT_TOKEN)

    # PERSISTANCE
    storage_path = settings.APP_DIR / "storage"
    my_persistence = PicklePersistence(filepath=storage_path)
    builder.persistence(my_persistence)

    # DEFAULTS
    defaults = Defaults(parse_mode=ParseMode.HTML)
    builder.defaults(defaults)

    # SETUP COMMANDS
    builder.post_init(setup_bot)

    application = builder.build()

    application.add_handler(conversation_handler)
    application.add_handler(admin_handler)

    # debug tools
    application.add_handler(CommandHandler("id", check_id))
    application.add_handler(CommandHandler("time", check_time))
    # application.add_handler(CommandHandler("language", ask_lang))
    application.add_error_handler(error_handler)  # type: ignore

    logger.debug("starting polling")
    application.run_polling()


if __name__ == "__main__":
    run_bot()
