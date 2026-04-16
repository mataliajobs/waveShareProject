import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from waveshare_epd import epd7in5_V2
from PIL import Image

print("[START] Strong clearing e-paper display...")

epd = epd7in5_V2.EPD()
epd.init()

# --- FORCE FULL CLEAN ---
print("[STEP] White pass...")
epd.display(epd.getbuffer(Image.new('1', (epd.width, epd.height), 255)))
time.sleep(2)

print("[STEP] Black pass...")
epd.display(epd.getbuffer(Image.new('1', (epd.width, epd.height), 0)))
time.sleep(2)

print("[STEP] Final white pass...")
epd.display(epd.getbuffer(Image.new('1', (epd.width, epd.height), 255)))
time.sleep(2)

print("[OK] Strong clear complete")

epd.sleep()
print("[DONE]")