import os
import time
import feedparser
import logging
from telegram import Bot
from flask import Flask

# Telegram & Feed setup
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RSS_URL = "https://rss.app/feeds/OUYIM0VGlxqKueAS.xml"

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)
sent_links = set()

@app.route('/')
def home():
    return "RSS Telegram Bot is running!"

def check_feed():
    global sent_links
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries[:5]:  # Limit to 5 entries per check
        if entry.link not in sent_links:
            message = f"**{entry.title}**\n{entry.link}"
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
            sent_links.add(entry.link)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        check_feed()
        time.sleep(600)  # Check every 10 minutes
