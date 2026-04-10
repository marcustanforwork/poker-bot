# Poker Staking Telegram Bot

A Telegram bot for Marcus to post live poker tournament updates to his staker group — formatted by Claude.

## Architecture

```
Marcus (DM) → Bot → claude -p "..." → Formatted card → Staker Group
```

Marcus inputs a compact template in a private DM. The bot passes it to `claude -p` which formats it into a polished Telegram card. The card is posted to the staker group. Stakers never see raw input.

## Commands

| Command | Description |
|---------|-------------|
| `/template` | Get both input templates in DM |
| `/hand` | Post a hand report to the staker group (Task 2) |
| `/status` | Post a tournament status update to the staker group (Task 2) |

All commands are DM-only. Commands sent in group chat are silently ignored.

---

## Prerequisites

- Python 3.11+
- `claude` CLI installed and authenticated (`claude --version` must work)
- A Telegram bot token (see BotFather setup below)
- The bot added to your staker group as an admin

---

## BotFather Setup

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts to name your bot
3. Copy the bot token — this is your `TELEGRAM_BOT_TOKEN`

---

## Getting Your IDs

### TELEGRAM_GROUP_CHAT_ID

1. Add the bot to your staker group as an admin
2. Send any message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find `"chat":{"id":...}` — it will be a negative number like `-1001234567890`

### AUTHORIZED_USER_ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It replies with your numeric user ID

---

## Local Development Setup

```bash
git clone https://github.com/<your-username>/poker-bot.git
cd poker-bot
cp .env.example .env
# fill in .env with your values
pip install -r requirements.txt
python bot.py
```

Test: send `/template` to your bot in DM — should return both templates with field guide.

> Note: `/hand` and `/status` are stubs until Task 2.

---

## Beelink Deployment

```bash
git clone https://github.com/<your-username>/poker-bot.git
cd poker-bot
pip install -r requirements.txt
cp .env.example .env
nano .env        # fill in values
python3 bot.py   # smoke test — send /template to confirm
```

Then follow the systemd setup below.

---

## Systemd Service (Task 3)

Create `/etc/systemd/system/pokerbot.service`:

```ini
[Unit]
Description=Poker Staking Telegram Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=marcus
WorkingDirectory=/home/marcus/poker-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Replace `marcus` with your actual Linux username.

```bash
sudo systemctl daemon-reload
sudo systemctl enable pokerbot
sudo systemctl start pokerbot
sudo systemctl status pokerbot
```

### Useful Ops Commands

```bash
sudo journalctl -u pokerbot -f        # live logs
sudo journalctl -u pokerbot -n 50     # last 50 lines
sudo systemctl stop pokerbot
sudo systemctl restart pokerbot
sudo systemctl is-enabled pokerbot
```

---

## Updating the Bot

When changes are pushed to GitHub, deploy on the Beelink:

```bash
cd /home/marcus/poker-bot
git pull origin main
sudo systemctl restart pokerbot
```

---

## Troubleshooting

- **Bot not responding**: `sudo systemctl status pokerbot`
- **Claude errors**: `sudo journalctl -u pokerbot -n 50`
- **MarkdownV2 errors**: handlers fall back to plain text automatically (Task 3)
