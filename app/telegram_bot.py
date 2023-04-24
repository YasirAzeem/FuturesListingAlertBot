import asyncio
from aiogram import Bot, Dispatcher, types
from .models import Listing, Session
from .settings import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def send_reminders():
    while True:
        session = Session()
        # Query the database for listings, calculate remaining time,
        # and send reminders accordingly
        # (2 days, 1 day, 12 hours, 6 hours, 3 hours, 1 hour, 30 minutes, 5 minutes, and live)
        pass

async def on_startup(dp):
    await bot.send_message(chat_id=YOUR_CHAT_ID, text="Bot has been started")

async def on_shutdown(dp):
    await bot.send_message(chat_id=YOUR_CHAT_ID, text="Bot has been stopped")

if __name__ == "__main__":
    from aiogram import executor
    from . import exchange_scrapers

    # Schedule scraping functions for each exchange
    # e.g., asyncio.create_task(scrape_binance())

    # Start the bot and send reminders
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
