from telegram import Update
from telegram.ext import ContextTypes
from auth import is_authorized_private


async def hand_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized_private(update):
        return
    await update.message.reply_text("⚙️ /hand not yet implemented — coming in Task 2.")
