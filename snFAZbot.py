import logging
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
TOKEN = "8874266093:AAHXCgGS_VkfSJ3XBBocucSZuN6AYhwlWRM"

def fetch_stories(username):
    url = f"https://storysharing.snapchat.com/v1/fetchStory?id={username}&type=NAME"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X)"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json().get("story", {}).get("snaps", [])
    except: return []
    return []

async def start(update, context):
    await update.message.reply_text("👻 البوت جاهز! أرسل اليوزر:")

async def handle_message(update, context):
    user = update.message.text.strip().lower().replace("@", "")
    await update.message.reply_text(f"⏳ جاري البحث...")
    snaps = fetch_stories(user)
    if not snaps:
        await update.message.reply_text("❌ لم أجد سنابات.")
        return
    for s in snaps:
        url = s.get("media", {}).get("mediaUrl") or s.get("media", {}).get("zippedMediaUrl")
        if url:
            try:
                if "mp4" in url.lower(): await update.message.reply_video(url)
                else: await update.message.reply_photo(url)
            except: pass

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 البوت بدأ العمل بأسلوب Polling...")
    app.run_polling()
