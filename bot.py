import os
from dotenv import load_dotenv
import logging

from telegram.ext import ApplicationBuilder, CommandHandler

from handlers import start, download_mp3

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

start_handler = CommandHandler("start", start)
download_mp3_handler = CommandHandler("download_mp3", download_mp3)

application.add_handler(start_handler)
application.add_handler(download_mp3_handler)

application.run_polling()