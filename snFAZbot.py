$pythonCode = 'import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = "8874266093:AAHXCgGS_VkfSJ3XBBocucSZuN6AYhwlWRM"

def fetch_via_global_net(username):
    media_urls = []
    url = f"https://api.allorigins.win/get?url={requests.utils.quote(f''https://storysharing.snapchat.com/v1/fetchStory?id={username}&type=NAME'')}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            import json
            contents = response.json().get("contents", "{}")
            response_data = json.loads(contents)
            story = response_data.get("story", {})
            snaps = story.get("snaps", [])
            for snap in snaps:
                media_info = snap.get("media", {})
                media_url = media_info.get("mediaUrl") or media_info.get("zippedMediaUrl")
                if media_url and media_url not in media_urls:
                    media_urls.append(media_url)
    except Exception as e:
        print(f"Error fetching: {e}")
    return media_urls

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👻 بوت FAZ السحابي المشغل على Render جاهز!\n\nأرسل يوزر السناب العام وسأجلب لك القصص مقاطع وصور فوراً 24 ساعة! 🚀")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip().lower().replace("@", "").split("/")[-1].split("?")[0]
    await update.message.reply_text(f"⏳ جاري الفحص والسحب الفوري لـ `{username}` عبر السحاب...")
    stories = fetch_via_global_net(username)
    if not stories:
        await update.message.reply_text("❌ لم أجد سنابات عامة نشطة حالياً، أو أن الحساب خاص.")
        return
    await update.message.reply_text(f"✅ تم العثور على {len(stories)} سناب نشط! جاري الإرسال...")
    for index, media_url in enumerate(stories, start=1):
        try:
            if "mp4" in media_url.lower() or "webm" in media_url.lower():
                await update.message.reply_video(video=media_url, caption=f"🎬 سناب {index}")
            else:
                await update.message.reply_photo(photo=media_url, caption=f"📸 سناب {index}")
        except Exception:
            await update.message.reply_text(f"🔗 رابط السناب المباشر {index}:\n{media_url}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 🌍 إعدادات الـ Webhook المتوافقة تماماً مع Render مجاناً
    PORT = int(os.environ.get("PORT", 8080))
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    
    if RENDER_EXTERNAL_URL:
        print(f"⚡ [🚀 LIVE] تشغيل البوت عبر الـ Webhook على الرابط: {RENDER_EXTERNAL_URL}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"{RENDER_EXTERNAL_URL}/{TELEGRAM_TOKEN}"
        )
    else:
        print("⚡ [🚀 LIVE] تشغيل البوت الاحتياطي عبر Polling...")
        app.run_polling()

if __name__ == "__main__":
    main()'; [System.IO.File]::WriteAllText((Get-Item .).FullName + "\snFAZbot.py", $pythonCode, [System.Text.Encoding]::UTF8)
