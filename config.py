import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_IDS = [int(chat_id.strip()) for chat_id in os.getenv('TELEGRAM_CHAT_IDS', '').split(',') if chat_id.strip()]

def validate_config():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
    if not TELEGRAM_CHAT_IDS:
        raise ValueError("TELEGRAM_CHAT_IDS not found in .env file")
