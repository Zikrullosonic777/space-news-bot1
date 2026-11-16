import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"].strip()
CHANNEL_ID = os.environ["CHANNEL_ID"].strip()

STATE_FILE = "last_post.txt"

def get_posted_ids():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_posted_id(item_id):
    with open(STATE_FILE, "a") as f:
        f.write(item_id + "\n")

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
    posted = get_posted_ids()

    # 1. Fetch NASA Astronomy Picture / Discovery of the Day (official NASA API)
    nasa_url = "https://nasa.gov"
    nasa_resp = requests.get(nasa_url, timeout=15).json()
    print("NASA API keys:", list(nasa_resp.keys()))
    if "title" in nasa_resp:
        nasa_id = "nasa_" + nasa_resp.get("date", nasa_resp["title"])
        if nasa_id not in posted:
            explanation = nasa_resp.get("explanation", "")[:300] + "..."
            img_url = nasa_resp.get("url", "https://nasa.gov")
            msg = (
                f"🔭 <b>[NASA Daily] {nasa_resp['title']}</b>\n\n"
                f"{explanation}\n\n"
                f"🖼 <a href='{img_url}'>View HD Image / Media</a>"
            )
            send_telegram_message(msg)
            save_posted_id(nasa_id)

    # 2. Fetch Upcoming SpaceX / NASA / Global Rocket Launches (Launch Library 2 API)
    launch_url = "https://thespacedevs.com"
    launch_resp = requests.get(launch_url, timeout=15).json()
    launches = launch_resp.get("results", [])
    print(f"Fetched {len(launches)} upcoming launches")

    for launch in reversed(launches):
        launch_id = "launch_" + str(launch["id"])
        if launch_id not in posted:
            name = launch.get("name", "Space Launch")
            provider = launch.get("launch_service_provider", {}).get("name", "Space Agency")
            net = launch.get("net", "TBD")
            mission_desc = (launch.get("mission") or {}).get("description", "Upcoming orbital mission.")[:220] + "..."
            msg = (
                f"🚀 <b>[Launch Alert] {name}</b>\n"
                f"🏢 <b>Agency:</b> {provider}\n"
                f"🕒 <b>Window (UTC):</b> {net}\n\n"
                f"{mission_desc}"
            )
            send_telegram_message(msg)
            save_posted_id(launch_id)

if __name__ == "__main__":
    main()
