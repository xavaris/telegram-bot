from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
TOPIC_WTB_ID = int(os.getenv("TOPIC_WTB_ID"))

def get_name(user):
    if user.username:
        return f"@{user.username}"
    return user.first_name or "Użytkownik"

async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.message.chat.type != "private":
        return

    user = update.message.from_user
    text = update.message.text
    name = get_name(user)

    await context.bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=TOPIC_WTB_ID,
        text=f"📥 WTB\n👤 {name}\n\n{text}"
    )

    await update.message.reply_text("✅ Wysłano do WTB.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_private_message))
    print("WTB BOT DZIAŁA")
    app.run_polling()

if __name__ == "__main__":
    main()
