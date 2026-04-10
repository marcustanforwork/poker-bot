from telegram import Update
from telegram.ext import ContextTypes
from auth import is_authorized_private

# ─────────────────────────────────────────────
# EDIT THESE TO CHANGE WHAT /template SENDS
# ─────────────────────────────────────────────

HAND_TEMPLATE = """/hand
stk 42000 | pos BTN
hnd AhKd
preflop: raised 2400, CO called
flop: Jh9c2d | bet 3200, CO raised 8400
turn: Ts | shoved 42000
river: 7c | (omit line if not reached)
vil1: CO | hnd JsJc
vil2: HJ | hnd 9h9d
res: both fold, won pot
note: nut straight draw semi bluff"""

# Minimal example shown alongside the full template
HAND_TEMPLATE_MINIMAL = """/hand
stk 15000 | pos SB
hnd QsQh
preflop: 3bet 2400, BB called
res: won at showdown"""

STATUS_TEMPLATE = """/status
event: Main Event Day 1K | buyin: 1100usd
stk: 87500 | blinds: 600/1200 lvl 12
left: 48/312
pos: top 15
bubble: 30 spots ITM, 18 remain
next: 1800usd at 18th | ft: 45000usd
note: table passive, feeling good"""

HAND_FIELD_GUIDE = """*HAND fields:*
`stk` = your chip stack
`pos` = position — BTN CO HJ MP EP SB BB
`hnd` = your hole cards (Ah=A♥ Kd=K♦ Tc=T♣ 9s=9♠)

*Streets* — only include streets you played:
`preflop` = preflop action
`flop` = 3 board cards | action
`turn` = 1 card | action
`river` = 1 card | action (omit line if not reached)

*Villains:*
`vil` = single villain (position + action)
`vil1` / `vil2` etc = multiple villains
Add `| hnd Xx Xx` to show their cards → bot shows equity %
Omit `hnd` if cards unknown → no equity shown

*Optional:*
`res` = result (required)
`note` = your read on the hand (optional)"""

STATUS_FIELD_GUIDE = """*STATUS fields:*
`event` = tournament name
`buyin` = buy-in amount
`stk` = current stack
`blinds` = blinds + level (e.g. 600/1200 lvl 12)
`left` = players remaining / total entries
`pos` = approx leaderboard position (optional)
`bubble` = bubble info (optional)
`next` = next payout spot (optional)
`ft` = final table prize (optional)
`note` = table notes (optional)"""

# ─────────────────────────────────────────────


async def template_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized_private(update):
        return

    await update.message.reply_text(
        "📋 *Your Input Templates*\nSend each filled\\-in to the bot in DM\\.",
        parse_mode="MarkdownV2"
    )

    await update.message.reply_text(
        "*— HAND REPORT (full) —*\n"
        f"`{HAND_TEMPLATE}`\n\n"
        "*— HAND REPORT (minimal) —*\n"
        f"`{HAND_TEMPLATE_MINIMAL}`",
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        HAND_FIELD_GUIDE,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        f"*— TOURNAMENT STATUS —*\n`{STATUS_TEMPLATE}`",
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        STATUS_FIELD_GUIDE,
        parse_mode="Markdown"
    )
