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
| `/hand` | Post a hand report to the staker group |
| `/status` | Post a tournament status update to the staker group |

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

## Local Development (main PC)

```bash
git clone https://github.com/marcustanforwork/poker-bot.git
cd poker-bot
cp .env.example .env
# fill in .env with your values
pip install -r requirements.txt
python bot.py
```

Test: send `/template` to your bot in DM — should return both templates with field guide.

---

## Beelink Deployment

### 1. Clone and install

```bash
git clone https://github.com/marcustanforwork/poker-bot.git
cd poker-bot
pip install -r requirements.txt
```

### 2. Create .env

```bash
cp .env.example .env
nano .env
```

Fill in:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_GROUP_CHAT_ID=-100xxxxxxxxxx
AUTHORIZED_USER_ID=your_numeric_telegram_id
```

### 3. Smoke test

```bash
python3 bot.py
```

Send `/template` in DM — if it responds, the bot works on this machine. Ctrl+C to stop.

### 4. Install systemd service

A ready-to-use service file is included in the repo. Edit `User=` and `WorkingDirectory=` if your Linux username is not `marcus`:

```bash
sudo cp pokerbot.service /etc/systemd/system/pokerbot.service
sudo nano /etc/systemd/system/pokerbot.service   # update User= and WorkingDirectory= if needed
```

### 5. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable pokerbot
sudo systemctl start pokerbot
sudo systemctl status pokerbot
```

Should show `Active: active (running)`.

### 6. Verify after reboot

```bash
sudo reboot
# wait ~30 seconds
sudo systemctl status pokerbot
```

Send `/template` to confirm the bot is alive.

---

## Ops Reference

```bash
# Live log stream
sudo journalctl -u pokerbot -f

# Last 50 log lines
sudo journalctl -u pokerbot -n 50

# Log file (on the Beelink, in the repo folder)
tail -f /home/marcus/poker-bot/pokerbot.log

# Stop / restart
sudo systemctl stop pokerbot
sudo systemctl restart pokerbot

# Check auto-start on boot
sudo systemctl is-enabled pokerbot
```

---

## Updating the Bot

When changes are pushed to GitHub from the main PC, deploy on the Beelink:

```bash
cd /home/marcus/poker-bot
git pull origin main
sudo systemctl restart pokerbot
```

---

## Using the Bot

### /template
Sends both input templates to your DM. Save these to Telegram Saved Messages for quick access at the table.

### /hand — Hand Report

Fill in the template and send in DM:

```
/hand
stk 42000 | pos BTN | pot 8400
hnd AhKd | brd Jh9c2dTs
vil: CO r5200
act: shoved 42000
res: villain fold, won pot
note: nut straight draw semi bluff
```

With villain cards known (shows equity):
```
/hand
stk 42000 | pos BTN | pot 8400
hnd AhKd | brd Jh9c2dTs
vil1: CO r5200 hnd JsJc
vil2: HJ hnd 9h9d
act: shoved 42000
res: both fold
```

### /status — Tournament Status

```
/status
event: Main Event Day 1K | buyin: 1100usd
stk: 87500 | blinds: 600/1200 lvl 12
left: 48/312
pos: top 15
bubble: 30 spots ITM, 18 remain
next: 1800usd at 18th | ft: 45000usd
note: table passive, feeling good
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Bot not responding | `sudo systemctl status pokerbot` |
| Claude errors | `sudo journalctl -u pokerbot -n 50` |
| MarkdownV2 formatting rejected | Handlers auto-retry as plain text |
| Bot crashes on start | Check `.env` has all three values set |
