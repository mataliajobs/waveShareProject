import sys
import os
from datetime import datetime
import calendar

# ✅ Use local lib folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont

# Initialize display
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()

# Create canvas
image = Image.new('1', (epd.width, epd.height), 255)
draw = ImageDraw.Draw(image)

# Load fonts
font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 64)
font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)

# Dimensions
width = epd.width
height = epd.height

left_width = int(width * 0.65)

# Draw borders
draw.rectangle((0, 0, left_width, height), outline=0)
draw.rectangle((left_width, 0, width, height//2), outline=0)
draw.rectangle((left_width, height//2, width, height), outline=0)

# -------------------------
# 📅 CALENDAR (LEFT PANEL)
# -------------------------
now = datetime.now()
month_name = now.strftime("%B %Y")

draw.text((20, 10), month_name, font=font_medium, fill=0)

cal = calendar.monthcalendar(now.year, now.month)

start_y = 60
for week in cal:
    week_str = ""
    for day in week:
        if day == now.day:
            week_str += f"[{day:2}] "
        elif day == 0:
            week_str += "   "
        else:
            week_str += f"{day:2} "
    draw.text((20, start_y), week_str, font=font_small, fill=0)
    start_y += 30

# -------------------------
# 📋 WEEK TASKS (RIGHT TOP)
# -------------------------
week_tasks = [
    "Finish Project",
    "UI Improvements",
    "Test System",
    "Prepare Demo"
]

draw.text((left_width + 10, 10), "WEEK TASKS", font=font_medium, fill=0)

y = 60
for task in week_tasks:
    draw.text((left_width + 10, y), f"- {task}", font=font_small, fill=0)
    y += 30

# -------------------------
# 🗓 TODAY TASKS (RIGHT BOTTOM)
# -------------------------
today_tasks = [
    "Run Code",
    "Fix Bugs",
    "Finalize UI"
]

draw.text((left_width + 10, height//2 + 10), "TODAY", font=font_medium, fill=0)

y = height//2 + 60
for task in today_tasks:
    draw.text((left_width + 10, y), f"- {task}", font=font_small, fill=0)
    y += 30

# -------------------------
# 🕒 TIME DISPLAY
# -------------------------
time_str = now.strftime("%I:%M %p")
draw.text((width//2 - 140, height - 120), time_str, font=font_large, fill=0)

# -------------------------
# DISPLAY OUTPUT
# -------------------------
epd.display(epd.getbuffer(image))
epd.sleep()