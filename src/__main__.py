import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import Updater

from .admin import admin
from .conv_handler import conversation_handler
from .handlers import ask_lang
from .handlers import error
from .handlers import stop_bot

load_dotenv()


def main():
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(CommandHandler("stop", stop_bot))
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("language", ask_lang))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
