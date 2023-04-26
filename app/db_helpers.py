from app.models import Session, Listing



def add_listing(exchange, symbol, launch_time, message, url):
    # Create a new session
    session = Session()

    existing_listing = session.query(Listing).filter_by(symbol=symbol, launch_time=launch_time).first()

    # If there's no existing listing with the same symbol and launch_time, add the new listing
    if existing_listing is None:
        # Create a new Listing object
        listing = Listing(symbol=symbol, exchange=exchange, launch_time=launch_time, message=message, url=url)

        # Add the listing to the session and commit
        session.add(listing)
        session.commit()

    # Close the session
    session.close()



def get_messages_by_exchange(exchange):
    session = Session()
    messages = session.query(Listing).filter(Listing.exchange == exchange).all()
    return list(messages)