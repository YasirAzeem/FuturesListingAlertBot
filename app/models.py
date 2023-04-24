from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    exchange = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    message = Column(String, nullable=False)
    url = Column(String, nullable=False)
    new_listing = Column(Boolean, default=True)
    launch_time = Column(DateTime, nullable=False)

engine = create_engine("sqlite:///listings.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
