import os
from dotenv import load_dotenv
import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers import start, download_mp3, helper, undefined_commands

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).get_updates_http_version('1.1').http_version('1.1').build()

start_handler = CommandHandler("start", start)
download_mp3_handler = CommandHandler("download_mp3", download_mp3)
help_handler = CommandHandler("help", helper)
unknown_handler = MessageHandler(filters.COMMAND, undefined_commands)

application.add_handler(start_handler)
application.add_handler(download_mp3_handler)
application.add_handler(help_handler)
application.add_handler(unknown_handler)

application.run_polling()
