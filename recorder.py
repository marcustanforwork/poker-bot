import os
from datetime import datetime
from state import load_state, update_state

RECORDS_DIR = "records"


def _strip_markdownv2(text: str) -> str:
    """Convert MarkdownV2 to plain readable text for the record file."""
    return text.replace("\\", "").replace("*", "").replace("`", "")


def save_hand_record(raw_input: str, formatted_msg: str):
    """
    Appends a hand record to records/YYYY-MM-DD.md.
    Hand number is persisted in state.json across bot restarts.
    """
    os.makedirs(RECORDS_DIR, exist_ok=True)

    state = load_state()
    hand_number = state.get("hand_number", 0) + 1
    update_state("hand_number", hand_number)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    filename = os.path.join(RECORDS_DIR, f"{today}.md")

    plain = _strip_markdownv2(formatted_msg)
    is_new_file = not os.path.exists(filename)

    with open(filename, "a", encoding="utf-8") as f:
        if is_new_file:
            f.write(f"# Hand Records — {today}\n\n")
        f.write(f"## Hand #{hand_number} — {time_str}\n\n")
        f.write(f"### Raw Input\n```\n{raw_input}\n```\n\n")
        f.write(f"### Formatted Card\n{plain}\n\n---\n\n")
