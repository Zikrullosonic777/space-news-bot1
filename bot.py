import os
import feedparser
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# Official NASA Breaking News RSS (you can add more feeds to this list)
RSS_FEEDS = [
    "https://nasa.gov",
    "https://space.com"
]

STATE_FILE = "last_post.txt"

def get_posted_links():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_posted_link(link):
    with open(STATE_FILE, "a") as f:
        f.write(link + "\n")

def send_telegram_message(text):
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

def main():
    posted = get_posted_links()
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        # Check the 3 latest articles per feed
        for entry in reversed(feed.entries[:3]):
            if entry.link not in posted:
                message = f"🚀 <b>{entry.title}</b>\n\n🔗 <a href='{entry.link}'>Read full article</a>"
                send_telegram_message(message)
                save_posted_link(entry.link)

if __name__ == "__main__":
    main()
