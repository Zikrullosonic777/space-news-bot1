import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"].strip()
CHANNEL_ID = os.environ["CHANNEL_ID"].strip()

FEEDS = [
    ("NASA", "https://reddit.com"),
    ("SpaceX", "https://reddit.com")
]

HEADERS = {
    "User-Agent": "python:aerospace.news.uz:v1.0 (by /u/aerospace_news_uz)"
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
    for tag, feed_url in FEEDS:
        resp = requests.get(feed_url, headers=HEADERS, timeout=15)
        print(tag, "Status:", resp.status_code)
        posts = resp.json().get("data", {}).get("children", [])
        for post in reversed(posts):
            item = post["data"]
            if item.get("stickied"):
                continue
            link = item["url"]
            if link not in posted:
                title = item["title"]
                message = (
                    f"🚀 <b>[{tag}] {title}</b>\n\n"
                    f"🔗 <a href='{link}'>Read more / View media</a>"
                )
                send_telegram_message(message)
                save_posted_link(link)

if __name__ == "__main__":
    main()
