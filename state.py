import json
import os

STATE_FILE = "state.json"


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(data: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_state(key: str, value):
    state = load_state()
    state[key] = value
    save_state(state)
