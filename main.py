import os
import json
import requests
import asyncio
from io import BytesIO
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    ContextTypes, 
    ChatJoinRequestHandler, 
    CommandHandler
)

# ================= CONFIG =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# APK URL
APK_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/7e38f5ecef1fc80fdc6f3c4e3e1d148c6ab7da66/JAI~CLUB%20NUMBER%20HACK_1.0.apk"
# Updated Welcome Video URL
WELCOME_VIDEO_URL = "https://raw.githubusercontent.com/loda26616-a11y/Idk/0f77a786914d9b416a0594e417e34f74e2511055/vid-20260421-120333-320_pAPAEC87.mp4"

BOT_USERNAME = "KD_VIP_HACK_BOT"
ADMIN_ID = 7303219901  

WELCOME_VIDEO_CAPTION = (
    "💰How To Activate Vip Hack💰\n"
    "Pls Video Ko Pura Dekhna\n"
    "      💯 Setup Video 💯"
)

APK_CAPTION = (
    "💛 MAA KSM NUMBER HACK WIN 💛\n\n"
    "REGISTER LINK ⛏\n"
    "https://www.jaiclub26.com/#/register?invitationCode=418543742969\n\n"
    "DM FOR 𝐕𝐈𝐏 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 💎\n"
    "⏩ @KD_HACK_MANAGER\n"
    "⏩ @KD_HACK_MANAGER"
)

USERS_FILE = "users.json"

# ================= CACHE =================
APK_FILE_ID_CACHE = None 
VIDEO_FILE_ID_CACHE = None 

# ================= DATA MANAGEMENT =================
def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f: return json.load(f)
    except: pass
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f: json.dump(users, f, indent=2)

def add_user(user):
    users = load_users()
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id, "username": user.username, 
            "first_name": user.first_name, "joined_at": datetime.now().isoformat()
        })
        save_users(users)

# ================= SEND MEDIA LOGIC =================
async def send_apk(user_id, context):
    global APK_FILE_ID_CACHE
    try:
        if APK_FILE_ID_CACHE:
            await context.bot.send_document(chat_id=user_id, document=APK_FILE_ID_CACHE, caption=APK_CAPTION)
        else:
            res = requests.get(APK_URL, timeout=120)
            res.raise_for_status()
            file = BytesIO(res.content)
            file.name = "JAI_CLUB_NUMBER_HACK.apk" 
            msg = await context.bot.send_document(chat_id=user_id, document=file, caption=APK_CAPTION)
            APK_FILE_ID_CACHE = msg.document.file_id 
    except Exception as e:
        print(f"APK Error: {e}")

async def send_welcome_video(user_id, context):
    global VIDEO_FILE_ID_CACHE
    try:
        if VIDEO_FILE_ID_CACHE:
            await context.bot.send_video(chat_id=user_id, video=VIDEO_FILE_ID_CACHE, caption=WELCOME_VIDEO_CAPTION)
        else:
            # Video direct URL se download karke upload hogi
            res = requests.get(WELCOME_VIDEO_URL, timeout=120)
            res.raise_for_status()
            video_file = BytesIO(res.content)
            video_file.name = "welcome_video.mp4"
            msg = await context.bot.send_video(chat_id=user_id, video=video_file, caption=WELCOME_VIDEO_CAPTION)
            VIDEO_FILE_ID_CACHE = msg.video.file_id
    except Exception as e:
        print(f"Video Error: {e}")

# ================= HANDLERS =================
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    try:
        add_user(user)
        # 1. Nayi Video Bhejna
        await send_welcome_video(user.id, context)
        # 2. APK Bhejna
        await send_apk(user.id, context)
    except: pass

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return 
    users = load_users()
    await update.message.reply_text(f"📊 **STATS**\nTotal Users: {len(users)}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not update.message.reply_to_message: return
    users = load_users()
    msg = update.message.reply_to_message
    sent = 0
    status_msg = await update.message.reply_text("🚀 Broadcasting...")
    for u in users:
        try:
            await msg.copy(chat_id=u["id"])
            sent += 1
            await asyncio.sleep(0.05)
        except: continue
    await status_msg.edit_text(f"✅ Sent to {sent} users.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user)
    await update.message.reply_text(f"Welcome {user.first_name}! Processing your request...")
    await send_welcome_video(user.id, context)
    await send_apk(user.id, context)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(join_request))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    
    print(f"Bot @{BOT_USERNAME} updated with new video URL.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
