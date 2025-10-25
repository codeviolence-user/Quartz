import mss
from pynput import keyboard, mouse
from PIL import Image
import io
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScreenCapture:
    def __init__(self):
        self.points = []
        self.f_pressed = False
        self.callback = None

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char == 'f':
                self.f_pressed = True
        except AttributeError:
            pass
        if key == keyboard.Key.esc:
            return False

    def on_release(self, key):
        try:
            if hasattr(key, 'char') and key.char == 'f':
                self.f_pressed = False
        except AttributeError:
            pass

    def on_click(self, x, y, button, pressed):
        if pressed and self.f_pressed and button == mouse.Button.left:
            self.points.append((x, y))
            logging.info(f"Point {len(self.points)} captured: ({x}, {y})")

            if len(self.points) == 2:
                screenshot = self.take_screenshot()
                self.points = []
                if self.callback:
                    self.callback(screenshot)

    def take_screenshot(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]

        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": width, "height": height}
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            logging.info(f"Screenshot captured: {width}x{height} at ({left}, {top})")
            return img_byte_arr
