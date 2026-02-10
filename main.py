import os
import asyncio
import time
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask('')
@app.route('/')
def home(): return "1winviews is Live! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURATION CHECK ---
def get_env(name, is_int=False):
    val = os.environ.get(name)
    if not val:
        logger.error(f"❌ ERROR: Environment Variable '{name}' missing hai!")
        return None
    return int(val) if is_int else val

API_ID = get_env("API_ID", True)
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")
SESSION_STRING = get_env("SESSION_STRING")
ADMIN_ID = get_env("ADMIN_ID", True)

if not all([API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, ADMIN_ID]):
    logger.error("❌ Kuch variables missing hain. Bot start nahi ho sakta.")
    exit(1)

bot = Client("bridge_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    Thread(target=run_web).start()
    logger.info("✅ Sab sahi hai! Bot start ho raha hai...")
    bot.run()
