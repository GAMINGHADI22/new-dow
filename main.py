import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8659260396:AAHVelixrAQiqvmfLO1kG4kVCQpAoTx73lo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 PRO Video Downloader Bot\n\n"
        "YouTube/TikTok link পাঠাও।\n"
        "Bot direct video send করবে।"
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not ("youtube.com" in url or "youtu.be" in url or "tiktok.com" in url):
        await update.message.reply_text("❌ YouTube/TikTok link পাঠাও।")
        return

    msg = await update.message.reply_text("⏳ Download হচ্ছে...")

    try:
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
            "max_filesize": 45 * 1024 * 1024,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await msg.edit_text("📤 Telegram এ পাঠাচ্ছি...")

        with open(file_path, "rb") as video:
            await update.message.reply_video(video=video, caption="✅ Done")

        os.remove(file_path)

    except Exception as e:
        await msg.edit_text("❌ Download failed.\n\n" + str(e)[:250])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
