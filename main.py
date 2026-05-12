import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot

# ================= CONFIG =================
# Ab token GitHub par nahi dikhega, Vercel Secrets se aayega
BOT_TOKEN = os.getenv("BOT_TOKEN")

APK_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/2301c244938dcdaa227fc13913abeca114beae95/JAI~CLUB%20NUMBER%20HACK_1.0.apk"
PHOTO_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/69738a5485ee3039cff79f9974ccc6de0b75e494/IMG_20260511_111128_792.jpg"

# Header Layout (3 + 4 + 4)
APK_CAPTION = (
    "<tg-emoji emoji-id='5969535994867749505'>🔠</tg-emoji> <tg-emoji emoji-id='5972019031425683213'>🔠</tg-emoji> <tg-emoji emoji-id='5969897592459366058'>🔠</tg-emoji>    " 
    "<tg-emoji emoji-id='5971996336818491960'>🔠</tg-emoji> <tg-emoji emoji-id='5969928280000695552'>🔠</tg-emoji> <tg-emoji emoji-id='5972235673871060829'>🔠</tg-emoji> <tg-emoji emoji-id='5969920372965904377'>🔠</tg-emoji>    " 
    "<tg-emoji emoji-id='5969666596233290681'>🔠</tg-emoji> <tg-emoji emoji-id='5972019031425683213'>🔠</tg-emoji> <tg-emoji emoji-id='5971996336818491960'>🔠</tg-emoji> <tg-emoji emoji-id='5969896827955187163'>🔠</tg-emoji>\n\n"
    "𝟭𝟬𝟬% 𝗡𝘂𝗺𝗯𝗲𝗿 𝗛𝗮𝗰𝗸 💥\n\n𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿𝘀 💎\n\n𝟭𝟬𝟬% 𝗟𝗼𝘀𝘀 𝗥𝗲𝗰𝗼𝘃𝗲𝗿 𝗚𝘂𝗮𝗿𝗮𝗻𝘁𝗲𝗲 🛡\n\n𝗙𝗼𝗿 𝗛𝗲𝗹𝗽 ➡️ @KD_HACK_MANAGER ✅"
)

app = Flask(__name__)

async def send_to_user(user_id):
    # Function ke andar bot initialize kar rahe hain fresh token ke saath
    bot = Bot(token=BOT_TOKEN)
    try:
        # Document (APK)
        await bot.send_document(
            chat_id=user_id, 
            document=APK_URL, 
            filename="JAI_CLUB_HACK.apk", 
            caption=APK_CAPTION, 
            parse_mode="HTML"
        )
        # Photo
        await bot.send_photo(
            chat_id=user_id, 
            photo=PHOTO_URL, 
            caption="💎 BEST HACK AND GENUINE STREAK WINNING 💎", 
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error in send_to_user: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        try:
            bot = Bot(token=BOT_TOKEN)
            update = Update.de_json(request.get_json(force=True), bot)
            
            if update.chat_join_request:
                user_id = update.chat_join_request.from_user.id
                # Vercel synchronous environment fix
                asyncio.run(send_to_user(user_id))
                
            return "OK", 200
        except Exception as e:
            print(f"Webhook Error: {e}")
            return "Error", 500
    return "Forbidden", 403

@app.route('/')
def index():
    return "Bot is Running Securely", 200
