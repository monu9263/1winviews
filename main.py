import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- 1. LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "1winviews is Live! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 3. CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION_STRING = os.environ.get("SESSION_STRING")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
SUB_LINK_CODE = "fz8rfeqN8zor"

# --- 4. CLIENTS ---
# Bot Client (For Creators)
bot = Client("creator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# Userbot Client (For LabViews Sync)
userbot = Client("user_relay", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- 5. BOT HANDLERS ---
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    logger.info(f"📩 Message received from: {message.from_user.id}")
    if message.from_user.id == ADMIN_ID:
        await message.reply("Bhai, Main Zinda Hoon! 🚀\nAapka account officially link ho gaya hai.")
    else:
        await message.reply(f"⚠️ Aap approved nahi hain. Aapki ID: `{message.from_user.id}`")

# --- 6. MAIN RUNNER ---
async def main():
    # Web server start karein taaki Render kill na kare
    Thread(target=run_web).start()
    
    logger.info("🚀 Starting Bots...")
    await bot.start()
    await userbot.start()
    
    # LabViews Subordinate Sync
    logger.info("🔗 Linking Userbot to LabViews...")
    await userbot.send_message("LabViews_bot", f"/start {SUB_LINK_CODE}")
    
    logger.info("✅ SUCCESS: Both bots are running!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
