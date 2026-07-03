import logging
import requests
import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
TOKEN = "8874266093:AAHXCgGS_VkfSJ3XBBocucSZuN6AYhwlWRM"

def fetch_stories(username):
    # اتصال مباشر بسناب شات مع تمويه User-Agent
    url = f"https://storysharing.snapchat.com/v1/fetchStory?id={username}&type=NAME"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": "https://storysharing.snapchat.com/"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return data.get("story", {}).get("snaps", [])
    except Exception as e:
        print(f"Direct connection error: {e}")
    return []

async def start(update, context):
    await update.message.reply_text("👻 بوت FAZ مباشر الآن!")

async def handle_message(update, context):
    user = update.message.text.strip().lower().replace("@", "")
    await update.message.reply_text(f"⏳ جاري سحب سنابات {user}...")
    snaps = fetch_stories(user)
    if not snaps:
        await update.message.reply_text("❌ لم أجد سنابات (قد يكون الحساب خاص أو لا يوجد سنابات).")
        return
    for s in snaps:
        url = s.get("media", {}).get("mediaUrl") or s.get("media", {}).get("zippedMediaUrl")
        if url:
            try:
                if "mp4" in url.lower(): await update.message.reply_video(url)
                else: await update.message.reply_photo(url)
            except: pass

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Active")

def run_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleServer)
    server.serve_forever()

if __name__ == '__main__':
    Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
