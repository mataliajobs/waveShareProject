import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from waveshare_epd import epd7in5_V2
from PIL import Image

print("[START] Deep cleaning display...")

epd = epd7in5_V2.EPD()
epd.init()

white = Image.new('1', (epd.width, epd.height), 255)
black = Image.new('1', (epd.width, epd.height), 0)

# Repeat cycle 2–3 times
for i in range(3):
    print(f"[CYCLE {i+1}] White")
    epd.display(epd.getbuffer(white))
    time.sleep(2)

    print(f"[CYCLE {i+1}] Black")
    epd.display(epd.getbuffer(black))
    time.sleep(2)

# Final white
print("[FINAL] White clean")
epd.display(epd.getbuffer(white))
time.sleep(2)

print("[OK] Deep clean complete")
epd.sleep()