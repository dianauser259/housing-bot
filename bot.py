import asyncio
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.saga.hamburg/immobiliensuche?kategorie=APARTMENT"

known_ads = set()

def fetch_ads():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    ads = []
    for link in soup.select("a.teaser"):
        href = link.get("href")
        if href and href not in known_ads:
            known_ads.add(href)
            ads.append("https://www.saga.hamburg" + href)
    return ads

async def main():
    bot = Bot(token=TOKEN)
    while True:
        new_ads = fetch_ads()
        for ad in new_ads:
            await bot.send_message(chat_id=CHAT_ID, text=ad)
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
