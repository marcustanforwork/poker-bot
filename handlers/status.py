from telegram import Update
from telegram.ext import ContextTypes
from auth import is_authorized_private


async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized_private(update):
        return
    await update.message.reply_text("⚙️ /status not yet implemented — coming in Task 2.")
