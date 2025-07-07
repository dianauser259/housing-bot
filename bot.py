import asyncio
from telegram import Bot

TOKEN = "8042937179:AAE9QPM8AtHkJhhBmiSjeroHZMIh2nnQO3w"

async def main():
    bot = Bot(token=TOKEN)
    updates = await bot.get_updates()
    for update in updates:
        print("chat_id:", update.message.chat.id)

if __name__ == "__main__":
    asyncio.run(main())
