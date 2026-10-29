import json
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# بيانات حسابك الشخصي (UserBot)
API_ID = 34755772       # حط الـ API ID بتاعك هنا
API_HASH = "f522c73accfdcdf3df061155fef7fceb" # حط الـ API HASH بتاعك هنا

# بيانات بوتك العادي (من BotFather)
BOT_TOKEN = "9240502823:AAGE_X1av05CkD6YmGG29fKX4a0hjsfal1U"
YOUR_TELEGRAM_ID = 8902745367  # حط الآيدي الشخصي بتاعك هنا عشان البوت يبعتلك عليه

app = Client("my_key_extractor_session", api_id=API_ID, api_hash=API_HASH)

TARGET_CHANNELS = ["rezzxmods", "mmjjknnjjj"]
KEYS_FILE = "sent_keys.json"

# دالة لتحميل المفاتيح القديمة عشان منع التكرار
def load_sent_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r") as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()

# دالة لحفظ المفتاح الجديد
def save_sent_key(key):
    sent_keys = load_sent_keys()
    sent_keys.add(key)
    with open(KEYS_FILE, "w") as f:
        json.dump(list(sent_keys), f)

@app.on_message(filters.chat(TARGET_CHANNELS) & filters.text)
async def extract_keys(client: Client, message: Message):
    text = message.text
    
    if "REZZX-" in text:
        lines = text.split("\n")
        keys = [line.strip() for line in lines if line.strip().startswith("REZZX-")]
        
        sent_keys = load_sent_keys()
        new_keys = [k for k in keys if k not in sent_keys]
        
        if new_keys:
            # استخدام البوت الخاص بك (@hackkeys_bot) لإرسال الرسائل
            async with Client("bot_sender_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as bot:
                await bot.send_message(YOUR_TELEGRAM_ID, f"🚨 **تم رصد {len(new_keys)} مفتاح جديد!**")
                
                for key in new_keys:
                    # إضافة زر نسخ سريع مع كل مفتاح
                    keyboard = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("📋 نسخ المفتاح", copy_text=key)]]
                    )
                    await bot.send_message(
                        chat_id=YOUR_TELEGRAM_ID,
                        text=f"`{key}`",
                        reply_markup=keyboard
                    )
                    save_sent_key(key)

print("UserBot is running...")
app.run()
