import mss
from PIL import Image

def capture_screen(filename="screen.png"):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save(filename)

    return filename

