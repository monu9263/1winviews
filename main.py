import os
import asyncio
import time
import sqlite3
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# --- 1. ERROR LOGGING (Isse pata chalega galti kahan hai) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. WEB SERVER (Render Port Binding Fix) ---
app = Flask('')
@app.route('/')
def home(): return "1winviews Bot is Live! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Web Server on port {port}")
    app.run(host='0.0.0.0', port=port)

# --- 3. CONFIGURATION (With Safety Checks) ---
try:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    SESSION_STRING = os.environ.get("SESSION_STRING")
    ADMIN_ID = int(os.environ.get("ADMIN_ID"))
except Exception as e:
    logger.error(f"❌ Config Error: Environment Variables sahi se nahi bhare gaye! {e}")
    exit(1)

# --- 4. CLIENTS ---
bot = Client("bridge_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("user_bridge", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- 5. START LOGIC ---
if __name__ == "__main__":
    # Web server ko pehle start karte hain taaki Render "No port detected" na kahe
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    logger.info("--- Starting Bot ---")
    try:
        bot.run()
    except Exception as e:
        logger.error(f"❌ Bot Crash Error: {e}")
