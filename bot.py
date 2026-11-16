import os
import feedparser
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"].strip()
CHANNEL_ID = os.environ["CHANNEL_ID"].strip()

RSS_FEEDS = [
    "https://nasa.gov",
    "https://space.com",
    "https://spaceflightnow.com"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

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
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload).json()
    print("TELEGRAM RESPONSE:", response)
    if not response.get("ok"):
        raise RuntimeError(f"Telegram rejected it: {response}")

def main():
    posted = get_posted_links()
    for feed_url in RSS_FEEDS:
        print("Checking feed:", feed_url)
        resp = requests.get(feed_url, headers=HEADERS, timeout=15)
        feed = feedparser.parse(resp.content)
        print(f"Found {len(feed.entries)} articles")
        for entry in reversed(feed.entries[:2]):
            if entry.link not in posted:
                message = f"🚀 <b>{entry.title}</b>\n\n🔗 <a href='{entry.link}'>Read full article</a>"
                send_telegram_message(message)
                save_posted_link(entry.link)

if __name__ == "__main__":
    main()
