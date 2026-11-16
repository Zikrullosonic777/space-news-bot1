import os
import feedparser
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"].strip()
CHANNEL_ID = os.environ["CHANNEL_ID"].strip()

RSS_FEEDS = [
    "https://nasa.gov",
    "https://space.com"
]

def send_telegram_message(text):
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload).json()
    print("TELEGRAM RESPONSE:", response)
    if not response.get("ok"):
        raise RuntimeError(f"Telegram rejected it: {response}")

def main():
    feed = feedparser.parse(RSS_FEEDS[0])
    entry = feed.entries[0]
    message = f"🚀 <b>{entry.title}</b>\n\n🔗 <a href='{entry.link}'>Read full article</a>"
    send_telegram_message(message)

if __name__ == "__main__":
    main()
