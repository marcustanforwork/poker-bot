import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.hand import hand_handler
from handlers.status import status_handler
from handlers.template import template_handler

load_dotenv()

LOG_FILE = os.path.join(os.path.dirname(__file__), "pokerbot.log")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
)


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("hand", hand_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("template", template_handler))

    logging.info("Poker Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
