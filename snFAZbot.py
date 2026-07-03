import logging
import requests
import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# إعداد السجل
logging.basicConfig(level=logging.INFO)

# التوكن
TOKEN = "8874266093:AAHXCgGS_VkfSJ3XBBocucSZuN6AYhwlWRM"

# كود جلب السنابات
def fetch_stories(username):
    url = f"https://api.allorigins.win/get?url={requests.utils.quote(f'https://storysharing.snapchat.com/v1/fetchStory?id={username}&type=NAME')}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            import json
            data = json.loads(res.json().get("contents", "{}"))
            return data.get("story", {}).get("snaps", [])
    except: return []
    return []

# أوامر البوت
async def start(update, context):
    await update.message.reply_text("👻 بوت FAZ يعمل الآن في السحاب 24/7!")

async def handle_message(update, context):
    user = update.message.text.strip().lower().replace("@", "")
    await update.message.reply_text(f"⏳ جاري سحب سنابات {user}...")
    snaps = fetch_stories(user)
    if not snaps:
        await update.message.reply_text("❌ لا يوجد سنابات عامة.")
        return
    for s in snaps:
        url = s.get("media", {}).get("mediaUrl")
        if url:
            try:
                if "mp4" in url: await update.message.reply_video(url)
                else: await update.message.reply_photo(url)
            except: pass

# تزييف خادم ويب عشان Render يرضى
class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleServer)
    server.serve_forever()

if __name__ == '__main__':
    # تشغيل الخادم الوهمي في خلفية
    Thread(target=run_server, daemon=True).start()
    
    # تشغيل البوت بأسلوب كلاسيكي مستقر
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 البوت الآن يعمل!")
    app.run_polling()
