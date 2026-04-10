import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", "0"))


def is_authorized(update) -> bool:
    """Check if the sender is Marcus."""
    return update.effective_user.id == AUTHORIZED_USER_ID


def is_private_chat(update) -> bool:
    """Check if message is in a DM (not a group)."""
    return update.effective_chat.type == "private"


def is_authorized_private(update) -> bool:
    """Combined check — authorized user in private DM only."""
    return is_authorized(update) and is_private_chat(update)
