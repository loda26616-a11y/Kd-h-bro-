import os
import requests
from io import BytesIO
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")

APK_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/2301c244938dcdaa227fc13913abeca114beae95/JAI~CLUB%20NUMBER%20HACK_1.0.apk"
WELCOME_PHOTO_URL = "https://raw.githubusercontent.com/toptenowner999-maker/KD/69738a5485ee3039cff79f9974ccc6de0b75e494/IMG_20260511_111128_792.jpg"

APK_CAPTION = """
𝟭𝟬𝟬% 𝗡𝘂𝗺𝗯𝗲𝗿 𝗛𝗮𝗰𝗸 💥

𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿𝘀 💎

𝟭𝟬𝟬% 𝗟𝗼𝘀𝘀 𝗥𝗲𝗰𝗼𝘃𝗲𝗿 𝗚𝘂𝗮𝗿𝗮𝗻𝘁𝗲𝗲 🛡

𝗙𝗼𝗿 𝗛𝗲𝗹𝗽 ➡️ @KD_HACK_MANAGER ✅
"""

WELCOME_CAPTION = """
🤑 MEMBERS FEEDBACK 🤑

💎 BEST HACK AND GENUINE STREAK WINNING 💎

⬇️ PANNEL LINK ⬇️

https://t.me/m/kkE6P6nfZDhl
"""

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

telegram_app = Application.builder().token(BOT_TOKEN).build()

# ================= SEND FILES =================
async def send_assets(user_id):
    try:
        apk_data = requests.get(APK_URL).content
        photo_data = requests.get(WELCOME_PHOTO_URL).content

        await bot.send_document(
            chat_id=user_id,
            document=BytesIO(apk_data),
            filename="JAI_CLUB_HACK.apk",
            caption=APK_CAPTION,
        )

        await bot.send_photo(
            chat_id=user_id,
            photo=BytesIO(photo_data),
            caption=WELCOME_CAPTION,
        )

    except Exception as e:
        print(f"Error: {e}")

# ================= HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_assets(update.effective_user.id)

async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_join_request.from_user.id
    await send_assets(user_id)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(ChatJoinRequestHandler(join_request))

# ================= WEBHOOK =================
@app.route("/", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, bot)
    await telegram_app.initialize()
    await telegram_app.process_update(update)

    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot Running"

# ================= MAIN =================
if __name__ == "__main__":
    app.run()
