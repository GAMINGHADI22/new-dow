import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

print("🚀 Bot starting...")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not found")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot working! Link পাঠাও")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 Link পেয়েছি!")

def main():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

        print("✅ Bot running...")
        app.run_polling()

    except Exception as e:
        print("❌ ERROR:", e)

if __name__ == "__main__":
    main()
