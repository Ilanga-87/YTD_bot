import os
from dotenv import load_dotenv
import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from handlers import start, audio_url_handler, format_download_handler, helper, undefined_commands, language_handler

from manage_data import SELECT_FORMAT, SELECT_LANGUAGE

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).get_updates_http_version('1.1').http_version('1.1').build()

start_handler = CommandHandler("start", start)
lang_handler = CallbackQueryHandler(language_handler, pattern=f"^{SELECT_LANGUAGE}")
url_handler = MessageHandler(filters.TEXT, audio_url_handler)
formats_handler = CallbackQueryHandler(format_download_handler, pattern=f"^{SELECT_FORMAT}")

help_handler = CommandHandler("help", helper)
unknown_handler = MessageHandler(filters.COMMAND, undefined_commands)

application.add_handler(start_handler)
application.add_handler(lang_handler)
application.add_handler(url_handler)
application.add_handler(formats_handler)
application.add_handler(help_handler)
application.add_handler(unknown_handler)

application.run_polling()
