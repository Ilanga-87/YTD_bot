import os
from dotenv import load_dotenv
import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from handlers import start, audio, select_format, helper, undefined_commands

from manage_data import SELECT_FORMAT

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).get_updates_http_version('1.1').http_version('1.1').build()

start_handler = CommandHandler("start", start)
url_handler = MessageHandler(filters.TEXT, audio)
formats_handler = CallbackQueryHandler(select_format, pattern=f"^{SELECT_FORMAT}")

help_handler = CommandHandler("help", helper)
unknown_handler = MessageHandler(filters.COMMAND, undefined_commands)

application.add_handler(start_handler)
application.add_handler(url_handler)
application.add_handler(formats_handler)
application.add_handler(help_handler)
application.add_handler(unknown_handler)

application.run_polling()


# TODO: 1. Find a way to keep old keyboards working

# TODO: 3. Multilang

