import os
import asyncio
import time
import sqlite3
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SETTINGS & LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask('')
@app.route('/')
def home(): return "1winviews Multi-User Bot is Live! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. CONFIG & DB ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION_STRING = os.environ.get("SESSION_STRING")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
SUB_LINK_CODE = "fz8rfeqN8zor"

db = sqlite3.connect("creators.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, pages TEXT, status INTEGER)")
db.commit()

bot = Client("creator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("user_relay", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- 3. QUEUE & STATE ---
current_user = None
lock_time = 0
user_task = {} # Store what page a user is working on

# --- 4. ADMIN COMMANDS ---

@bot.on_message(filters.command("approve") & filters.user(ADMIN_ID))
async def approve_user(client, message):
    try:
        # Format: /approve 12345678 page1,page2
        _, uid, pages = message.text.split(" ", 2)
        cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, 1)", (int(uid), pages))
        db.commit()
        await message.reply(f"✅ User `{uid}` approve ho gaya.\nPages: `{pages}`")
        await bot.send_message(int(uid), "🎉 Admin ne aapko approve kar diya hai! `/start` dabayein.")
    except:
        await message.reply("❌ Format: `/approve user_id page1,page2` (बिना स्पेस के कोमा लगाएं)")

# --- 5. CREATOR FLOW ---

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    uid = message.from_user.id
    cursor.execute("SELECT pages, status FROM users WHERE id=?", (uid,))
    res = cursor.fetchone()

    if uid == ADMIN_ID or (res and res[1] == 1):
        # Admin gets all pages, Creators get assigned pages
        allowed_pages = res[0].split(",") if res else "All"
        await message.reply("🔄 LabViews se aapke pages fetch ho rahe hain...")
        
        # Automatic Button Fetching from LabViews
        async with userbot:
            await userbot.send_message("LabViews_bot", "My social media")
            await asyncio.sleep(1)
            await userbot.send_message("LabViews_bot", "India")
            await asyncio.sleep(1)
            await userbot.send_message("LabViews_bot", "Instagram Reels")
            await asyncio.sleep(1)
            await userbot.send_message("LabViews_bot", "Submit a video for review")
            await asyncio.sleep(2)
            
            history = userbot.get_chat_history("LabViews_bot", limit=1)
            keyboard = []
            async for msg in history:
                if msg.reply_markup:
                    for row in msg.reply_markup.inline_keyboard:
                        for btn in row:
                            # Filter: Sirf assigned pages dikhana
                            if allowed_pages == "All" or any(p.lower() in btn.text.lower() for p in allowed_pages):
                                if "Main menu" not in btn.text:
                                    keyboard.append([InlineKeyboardButton(btn.text, callback_data=f"set_{btn.text}")])
            
            await message.reply("Apna page select karein:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply(f"👋 Welcome! Aapki ID `{uid}` hai. Admin ko bhein taaki wo approve kar sakein.")

@bot.on_callback_query(filters.regex("^set_"))
async def select_page(client, callback):
    global current_user, lock_time
    uid = callback.from_user.id
    
    # Notice Feature: Wait system
    if current_user and current_user != uid and (time.time() - lock_time) < 300:
        await callback.answer("⏳ Abhi koi aur creator kaam kar raha hai. 5 min wait karein.", show_alert=True)
        return

    page = callback.data.split("_", 1)[1]
    user_task[uid] = page
    current_user = uid
    lock_time = time.time()
    
    await callback.message.edit(f"✅ Selected: **{page}**\n\nAb apni **Reel Link** bhejein. Bot 5 min ke liye aapke liye lock hai.")

@bot.on_message(filters.regex("instagram.com") & filters.private)
async def process_reel(client, message):
    global current_user
    uid = message.from_user.id
    
    if uid != current_user:
        await message.reply("⚠️ Pehle page select karein ya wait karein.")
        return

    status = await message.reply("🚀 Link LabViews par submit ho raha hai...")
    page = user_task.get(uid)
    
    async with userbot:
        await userbot.send_message("LabViews_bot", page)
        await asyncio.sleep(2)
        await userbot.send_message("LabViews_bot", "I added!")
        await asyncio.sleep(1)
        await userbot.send_message("LabViews_bot", message.text)
        
    await status.edit(f"🎉 **{page}** ke liye submission complete!\n\n#done #1winviews")
    current_user = None # Lock release

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.run()
