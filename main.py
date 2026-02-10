import os
import asyncio
import time
import logging
import sqlite3
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- WEB SERVER (For Render) ---
app = Flask('')
@app.route('/')
def home(): return "Creatorviews Bot is Live! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURATION (With Error Fix) ---
def get_env(name, is_int=False):
    val = os.environ.get(name)
    if not val:
        logger.error(f"❌ Environment Variable '{name}' missing hai! Render settings check karein.")
        return None
    return int(val) if is_int else val

API_ID = get_env("API_ID", True)
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")
SESSION_STRING = get_env("SESSION_STRING")
ADMIN_ID = get_env("ADMIN_ID", True)
SUB_LINK_CODE = "fz8rfeqN8zor" # Aapka subordinate code

if None in [API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, ADMIN_ID]:
    logger.error("❌ Kuch variables missing hain. Bot exit ho raha hai.")
    exit(1)

# --- CLIENTS ---
bot = Client("bridge_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("user_bridge", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- SUBORDINATE ACTIVATION ---
async def activate_subordinate():
    async with userbot:
        logger.info("🔗 Subordinate link activate kar raha hoon...")
        await userbot.send_message("LabViews_bot", f"/start {SUB_LINK_CODE}")
        logger.info("✅ Subordinate status linked!")

# --- START LOGIC ---
if __name__ == "__main__":
    # Web server start for Render
    Thread(target=run_web, daemon=True).start()
    
    # Run Subordinate activation once
    loop = asyncio.get_event_loop()
    loop.run_until_complete(activate_subordinate())
    
    logger.info("🚀 @Creatorviews_bot is starting...")
    bot.run()
