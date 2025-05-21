import os
import asyncio
import logging
import feedparser
from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import web
from html import escape

# Load env variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Must be an integer
RSS_URL = "https://rss.app/feeds/OUYIM0VGlxqKueAS.xml"

app = Client("rss_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
sent_links = set()

# Web server for uptime monitoring
async def handle(request):
    return web.Response(text="RSS Pyrogram Bot is live!")

async def run_web():
    server = web.Application()
    server.router.add_get("/", handle)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, port=int(os.environ.get("PORT", 8080)))
    await site.start()

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    await message.reply_text("Welcome to the RSS Feed Bot!\nYou'll receive automatic updates from the RSS feed.")

# RSS Feed Checker
async def rss_watcher():
    while True:
        feed = feedparser.parse(RSS_URL)
        for entry in feed.entries[:5]:
            if entry.link not in sent_links:
                title = escape(entry.title)
                link = escape(entry.link)
                text = f"<b>{title}</b>\n<a href=\"{link}\">Read More</a>"
                try:
                    await app.send_message(chat_id=CHAT_ID, text=text, parse_mode="html", disable_web_page_preview=False)
                    sent_links.add(entry.link)
                except Exception as e:
                    logging.error(f"Error sending feed item: {e}")
        await asyncio.sleep(600)  # Check every 10 mins

# Main async entry point
async def main():
    await app.start()
    await asyncio.gather(rss_watcher(), run_web())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
