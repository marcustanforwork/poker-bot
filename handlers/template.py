from telegram import Update
from telegram.ext import ContextTypes
from auth import is_authorized_private

HAND_TEMPLATE = """/hand
stk 42000 | pos BTN | pot 8400
hnd AhKd | brd Jh9c2dTs
vil: CO r5200
act: shoved 42000
res: villain fold, won pot
note: nut straight draw semi bluff"""

STATUS_TEMPLATE = """/status
event: Main Event Day 1K | buyin: 1100usd
stk: 87500 | blinds: 600/1200 lvl 12
left: 48/312
pos: top 15
bubble: 30 spots ITM, 18 remain
next: 1800usd at 18th | ft: 45000usd
note: table passive, feeling good"""

FIELD_GUIDE = """
*HAND fields:*
stk = my chip stack
pos = position (BTN/CO/HJ/MP/EP/SB/BB)
pot = pot size
hnd = hole cards (Ah=Ace♥ Kd=King♦ Tc=Ten♣ 9s=Nine♠)
brd = board cards (omit if preflop)
vil = villain position + action (optional)
act = my action
res = result
note = my read (optional)

*STATUS fields:*
event = tournament name
buyin = buy-in amount
stk = current stack
blinds = blinds + level
left = players left / total entries
pos = approx position (optional)
bubble = bubble info (optional)
next = next payout (optional)
ft = final table prize (optional)
note = player notes (optional)
"""


async def template_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized_private(update):
        return

    msg = (
        "📋 *Your Input Templates*\n\n"
        "*— HAND REPORT —*\n"
        f"`{HAND_TEMPLATE}`\n\n"
        "*— TOURNAMENT STATUS —*\n"
        f"`{STATUS_TEMPLATE}`\n\n"
        f"{FIELD_GUIDE}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")
