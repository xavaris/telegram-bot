from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import os
import time
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
TOPIC_WTB_ID = int(os.getenv("TOPIC_WTB_ID"))
TOPIC_WTS_ID = int(os.getenv("TOPIC_WTS_ID"))

COOLDOWN = 12 * 60 * 60  # 12h
AUTO_DELETE = 12 * 60 * 60  # 12h

# pamięć w RAM (wystarcza na Railway)
last_sent = {}
pending_choice = {}

def get_display_name(user):
    if user.username:
        return f"@{user.username}"
    return user.first_name or "Użytkownik"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *BOT OGŁOSZEŃ*\n\n"
        "Jak to działa:\n"
        "1️⃣ Napisz do mnie wiadomość (treść ogłoszenia)\n"
        "2️⃣ Wybierz *WTB* lub *WTS*\n"
        "3️⃣ Post pojawi się na grupie z Twoim nickiem\n\n"
        "⏱ Limit: 1 wiadomość co 12h\n"
        "🧹 Post znika po 12h\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    user_id = update.message.from_user.id
    now = time.time()

    if user_id in last_sent and now - last_sent[user_id] < COOLDOWN:
        remaining = int((COOLDOWN - (now - last_sent[user_id])) / 3600) + 1
        await update.message.reply_text(
            f"⏳ Limit 12h. Spróbuj za ~{remaining}h."
        )
        return

    pending_choice[user_id] = update.message.text

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📥 WTB", callback_data="WTB"),
            InlineKeyboardButton("📤 WTS", callback_data="WTS"),
        ]
    ])

    await update.message.reply_text(
        "Wybierz kategorię:",
        reply_markup=keyboard
    )

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    user_id = user.id

    if user_id not in pending_choice:
        await query.edit_message_text("❌ Brak treści do wysłania.")
        return

    text = pending_choice.pop(user_id)
    last_sent[user_id] = time.time()

    topic_id = TOPIC_WTB_ID if query.data == "WTB" else TOPIC_WTS_ID
    label = "WTB" if query.data == "WTB" else "WTS"
    name = get_display_name(user)

    sent = await context.bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=topic_id,
        text=f"🔔 *{label}*\n👤 {name}\n\n{text}",
        parse_mode="Markdown"
    )

    await query.edit_message_text("✅ Wysłano.")

    # auto-usuwanie po 12h
    await asyncio.sleep(AUTO_DELETE)
    try:
        await context.bot.delete_message(
            chat_id=GROUP_ID,
            message_id=sent.message_id
        )
    except:
        pass

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(handle_choice))

    print("Bot działa 24/7 (WTB/WTS, limit 12h, auto-delete 12h)")
    app.run_polling()

if __name__ == "__main__":
    main()
