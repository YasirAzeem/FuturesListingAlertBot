import asyncio
from aiogram import Bot, Dispatcher, types

from datetime import datetime, timedelta

from app.models import Listing, Session
from app.settings import TELEGRAM_TOKEN, CHAT_ID
from app.exchange_scrapers import run_all
from helpers.telegram_message import create_telegram_message


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def send_reminders():
    reminder_intervals = [
        timedelta(days=2),
        timedelta(days=1),
        timedelta(hours=12),
        timedelta(hours=6),
        timedelta(hours=3),
        timedelta(hours=1),
        timedelta(minutes=30),
        timedelta(minutes=5),
    ]

    while True:
        session = Session()
        now = datetime.datetime.utcnow()

        listings = session.query(Listing).all()
        for listing in listings:
            remaining_time = listing.launch_time - now
            if listing.new_listing:
                await bot.send_message(chat_id=CHAT_ID, text=create_telegram_message(listing))
                listing.new_listing = False
                session.commit()
            else:

                for interval in reminder_intervals:
                    if 0 <= remaining_time <= interval:
                        # message = f"Reminder: {listing.symbol} will be listed on {listing.exchange} in {remaining_time}. {listing.message}\n{listing.url}"
                        await bot.send_message(chat_id=CHAT_ID, text=create_telegram_message(listing))
                        break  # Avoid sending multiple reminders for the same listing

        await asyncio.sleep(60)

async def on_startup(dp):
    asyncio.create_task(run_all())
    asyncio.create_task(send_reminders())
    await bot.send_message(chat_id=CHAT_ID, text="Bot has been started")

async def on_shutdown(dp):
    await bot.send_message(chat_id=CHAT_ID, text="Bot has been stopped")

if __name__ == "__main__":
    from aiogram import executor
    from . import exchange_scrapers

    # Schedule scraping functions for each exchange
    # e.g., asyncio.create_task(scrape_binance())

    # Start the bot and send reminders
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
