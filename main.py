import asyncio
import logging
from pynput import keyboard, mouse
from capture import ScreenCapture
from ai import process_screenshot
from sender import send_to_telegram
from config import validate_config
import io

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_and_send(screenshot_bytes):
    try:
        ai_response = await process_screenshot(io.BytesIO(screenshot_bytes.read()))

        screenshot_bytes.seek(0)
        await send_to_telegram(screenshot_bytes, ai_response)

        logging.info("Processing completed successfully")
    except Exception as e:
        logging.error(f"Error in process_and_send: {e}")

def main():
    try:
        validate_config()

        print("""
 ██████╗ ██╗   ██╗ █████╗ ██████╗ ████████╗███████╗
██╔═══██╗██║   ██║██╔══██╗██╔══██╗╚══██╔══╝╚══███╔╝
██║   ██║██║   ██║███████║██████╔╝   ██║     ███╔╝
██║▄▄ ██║██║   ██║██╔══██║██╔══██╗   ██║    ███╔╝
╚██████╔╝╚██████╔╝██║  ██║██║  ██║   ██║   ███████╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
        """)

        logging.info("Quartz started. Press F+Click to select two points. Press ESC to exit.")

        capture = ScreenCapture()

        def on_screenshot_ready(screenshot):
            logging.info("Two points captured, processing screenshot...")
            asyncio.run(process_and_send(screenshot))

        capture.callback = on_screenshot_ready

        keyboard_listener = keyboard.Listener(
            on_press=capture.on_press,
            on_release=capture.on_release
        )
        mouse_listener = mouse.Listener(on_click=capture.on_click)

        keyboard_listener.start()
        mouse_listener.start()

        logging.info("Listeners started. Waiting for input...")

        keyboard_listener.join()

        logging.info("Quartz stopped")
    except Exception as e:
        logging.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
