import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = "8042937179:AAE9QPM8AtHkJhhBmiSjeroHZMIh2nnQO3w"
CHAT_ID = "7268470905"
URL = "https://www.saga.hamburg/immobiliensuche?kategorie=APARTMENT"

known_ads = set()

def fetch_ads():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    ads = []

    for item in soup.find_all("a", class_="teaser__link"):
        title = item.get_text(strip=True)
        href = item["href"]
        link = f"https://www.saga.hamburg{href}"
        ad_id = hash(link)
        ads.append((ad_id, title, link))

    return ads

async def notify(bot, ads):
    global known_ads
    new_ads = [ad for ad in ads if ad[0] not in known_ads]

    for ad_id, title, link in new_ads:
        msg = f"🏠 *Новое объявление:*\n[{title}]({link})"
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
        known_ads.add(ad_id)

async def main():
    bot = Bot(token=TOKEN)

    while True:
        try:
            ads = fetch_ads()
            await notify(bot, ads)
        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(300)  # каждые 5 минут

if __name__ == "__main__":
    asyncio.run(main())
