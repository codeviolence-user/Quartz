from aiogram import Bot
from aiogram.types import BufferedInputFile
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_to_telegram(image_bytes, ai_response):
    try:
        image_bytes.seek(0)
        image_data = image_bytes.read()

        input_file = BufferedInputFile(image_data, filename="screenshot.png")

        for chat_id in TELEGRAM_CHAT_IDS:
            try:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=input_file,
                    caption=f"<b>Ваше решение:</b>\n\n{ai_response}",
                    parse_mode="HTML"
                )
                logging.info(f"Message sent to chat_id: {chat_id}")
            except Exception as e:
                logging.error(f"Failed to send message to chat_id {chat_id}: {e}")

        logging.info("All messages sent successfully")
    except Exception as e:
        logging.error(f"Error sending to Telegram: {e}")
    finally:
        await bot.session.close()
