import datetime

def create_telegram_message(listing):
    emoji_clock = "\U0001F552"
    emoji_exchange = "\U0001F4B0"
    emoji_rocket = "\U0001F680"
    emoji_link = "\U0001F517"

    message = (
        f"{emoji_rocket} **New Listing Alert**\n\n"
        f"{emoji_exchange} **Exchange:** {listing.exchange}\n"
        f"**Symbol:** {listing.symbol}\n"
        f"{emoji_clock} **Launch Time:** {datetime.datetime.utcfromtimestamp(listing.launch_time/1000).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        f"{emoji_link} [More Info]({listing.url})\n\n"
        f"**_Message:_** {listing.message}"
    )

    return message