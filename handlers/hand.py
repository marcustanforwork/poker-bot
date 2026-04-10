import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

from auth import is_authorized_private
from claude_runner import run_claude
from prompts import build_hand_prompt

load_dotenv()
logger = logging.getLogger(__name__)
GROUP_CHAT_ID = int(os.getenv("TELEGRAM_GROUP_CHAT_ID", "0"))


async def hand_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized_private(update):
        return

    raw_input = update.message.text.partition("/hand")[2].strip()

    if not raw_input:
        await update.message.reply_text(
            "⚠️ No hand data provided\\.\n\nSend `/template` to get the input template\\.",
            parse_mode="MarkdownV2"
        )
        return

    ack = await update.message.reply_text("⏳ Formatting hand\\.\\.\\.", parse_mode="MarkdownV2")

    try:
        prompt = build_hand_prompt(raw_input)
        formatted_msg = run_claude(prompt)

        try:
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=formatted_msg,
                parse_mode="MarkdownV2"
            )
        except Exception as fmt_error:
            logger.warning(f"MarkdownV2 send failed ({fmt_error}), retrying as plain text")
            plain = formatted_msg.replace("*", "").replace("\\", "").replace("`", "")
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=plain)

        await ack.edit_text("✅ Hand posted to group\\!", parse_mode="MarkdownV2")

    except Exception as e:
        logger.error(f"hand_handler error: {e}")
        await ack.edit_text(
            f"⚠️ Failed to post hand\\.\n\nError: `{str(e)[:200]}`",
            parse_mode="MarkdownV2"
        )
