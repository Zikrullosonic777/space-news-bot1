import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"].strip()
CHANNEL_ID = os.environ["CHANNEL_ID"].strip()

# Free official Spaceflight News API (covers NASA, SpaceX, ESA, etc.)
API_URL = "https://spaceflightnewsapi.net"

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
    data = requests.get(API_URL, timeout=15).json()
    articles = data.get("results", [])
    print(f"Fetched {len(articles)} articles")

    if not articles:
        raise RuntimeError("No articles returned from API!")

    for article in reversed(articles):
        link = article["url"]
        if link not in posted:
            title = article["title"]
            summary = article.get("summary", "")[:220] + "..."
            source = article.get("news_site", "Space News")
            message = (
                f"🚀 <b>{title}</b>\n\n"
                f"{summary}\n\n"
                f"📡 <i>Source: {source}</i>\n"
                f"🔗 <a href='{link}'>Read full article</a>"
            )
            send_telegram_message(message)
            save_posted_link(link)

if __name__ == "__main__":
    main()
