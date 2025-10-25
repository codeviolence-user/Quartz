import google.generativeai as genai
from config import GEMINI_API_KEY
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

genai.configure(api_key=GEMINI_API_KEY)

async def process_screenshot(image_bytes):
    try:
        image_bytes.seek(0)
        img = Image.open(image_bytes)

        model = genai.GenerativeModel('gemini-2.5-pro')

        prompt = "Реши задание на этом скриншоте. Предоставь подробное решение."

        logging.info("Sending image to Gemini API...")
        response = model.generate_content([prompt, img])

        result = response.text
        logging.info("Received response from Gemini API")

        return result
    except Exception as e:
        logging.error(f"Error processing screenshot with Gemini: {e}")
        return f"Ошибка обработки: {str(e)}"
