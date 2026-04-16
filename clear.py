import sys
import os
import time

# Add Waveshare library path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from waveshare_epd import epd7in5_V2
from PIL import Image

print("[START] Clearing e-paper display...")

# Initialize display
epd = epd7in5_V2.EPD()
epd.init()

# Method 1: Official clear (recommended)
print("[STEP] Running epd.Clear()...")
epd.Clear()

# Optional: Extra assurance (force white frame)
print("[STEP] Forcing full white frame...")
white_image = Image.new('1', (epd.width, epd.height), 255)
epd.display(epd.getbuffer(white_image))

print("[OK] Display cleared to white")

# Sleep to protect panel
epd.sleep()

print("[DONE] Clear complete")