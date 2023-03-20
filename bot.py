import os
from dotenv import load_dotenv
import logging

from telegram.ext import ApplicationBuilder, CommandHandler

from handlers import start

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

start_handler = CommandHandler("start", start)

application.add_handler(start_handler)

application.run_polling()
