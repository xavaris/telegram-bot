from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
TOPIC_ID = int(os.getenv("TOPIC_ID"))

async def forward_to_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat.type == "private":
        await context.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=TOPIC_ID,
            text=update.message.text
        )
        await update.message.reply_text("✅ Wiadomość wysłana.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_topic))
    print("Bot działa 24/7 na Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()
