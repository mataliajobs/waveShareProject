import sys
import os
from datetime import datetime
import calendar

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Waveshare
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

print("[START] Calendar Dashboard")

# -------------------------
# GOOGLE AUTH
# -------------------------
def get_events():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=6,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])

events = get_events()
print(f"[INFO] Fetched {len(events)} events")

# -------------------------
# INIT DISPLAY
# -------------------------
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()

# -------------------------
# CANVAS
# -------------------------
image = Image.new('1', (epd.width, epd.height), 255)
draw = ImageDraw.Draw(image)

# Fonts
font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
font_day = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
font_date = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

# Dimensions
W = epd.width
H = epd.height

left_width = int(W * 0.7)

# -------------------------
# CALENDAR (LEFT 70%)
# -------------------------
now = datetime.now()
month_year = now.strftime("%B %Y")

draw.text((20, 10), month_year, font=font_title, fill=0)

days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
start_x = 40
start_y = 80
cell_w = (left_width - 60) // 7

for i, d in enumerate(days):
    draw.text((start_x + i * cell_w, start_y), d, font=font_day, fill=0)

cal = calendar.monthcalendar(now.year, now.month)

y = start_y + 40

for week in cal:
    for i, day in enumerate(week):
        x = start_x + i * cell_w

        if day != 0:
            if day == now.day:
                draw.rectangle((x-5, y-5, x+30, y+30), outline=0, width=2)
            draw.text((x, y), str(day), font=font_date, fill=0)

    y += 45

# -------------------------
# UPCOMING EVENTS (RIGHT 30%)
# -------------------------
draw.line((left_width, 0, left_width, H), fill=0, width=2)

draw.text((left_width + 10, 10), "EVENTS", font=font_title, fill=0)

y = 80

for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    title = event.get('summary', 'No Title')

    # shorten text
    text = f"- {title[:18]}"
    draw.text((left_width + 10, y), text, font=font_small, fill=0)
    y += 40

# -------------------------
# DISPLAY
# -------------------------
print("[STEP] Rendering display...")
epd.display(epd.getbuffer(image))
epd.sleep()

print("[DONE] Dashboard shown")