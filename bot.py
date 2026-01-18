from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ====== KONFIGURACJA ======
BOT_TOKEN = "8485283924:AAG6sf4mMFDsDKEYUvCwGW501rxd3qe3ne8"
GROUP_ID = -1003633468934      # ID GRUPY
TOPIC_ID = 16                  # ID TEMATU
# ==========================

async def forward_to_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tylko wiadomości prywatne
    if update.message.chat.type != "private":
        return

    text=f"📩 Od @{update.message.from_user.username}:\n\n{text}"

    if not text:
        await update.message.reply_text("❌ Tylko tekst.")
        return

    await context.bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=TOPIC_ID,
        text=f"📩 Nowa wiadomość:\n\n{text}"
    )

    await update.message.reply_text("✅ Wiadomość wysłana.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_topic))
    app.run_polling()

if __name__ == "__main__":
    main()
