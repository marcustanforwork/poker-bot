def build_hand_prompt(raw_input: str) -> str:
    """Build the full claude -p prompt for hand analysis. Implemented in Task 2."""
    return f"Format this poker hand for a Telegram staking group:\n\n{raw_input}"


def build_status_prompt(raw_input: str) -> str:
    """Build the full claude -p prompt for tournament status. Implemented in Task 2."""
    return f"Format this poker tournament update for a Telegram staking group:\n\n{raw_input}"
