from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
from urllib.parse import quote_plus

from src.clients.fixer import get_historical

Base = declarative_base()

class CurrencyRate(Base):
    __tablename__ = 'currency_rates3'

    id = Column(Integer, primary_key=True)
    base = Column(String)
    date = Column(DateTime)
    # rates
    GBP = Column(Float)
    USD = Column(Float)


# Assuming response_data contains the API response as a dictionary

encoded_password = quote_plus("Touc@n16")
connection_string = f"postgresql://georgegarforth:{encoded_password}@127.0.0.1:5434/postgres"
# Create a SQLAlchemy engine
engine = create_engine(connection_string)


# Establish connection to your PostgreSQL database

Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

start_date = datetime.datetime(2022, 1, 1)

for i in range(3):
    response_data = get_historical(start_date.strftime("%Y-%m-%d"), base="EUR")

    # Extract data from the API response
    data_to_insert = {
        'base': response_data['base'],
        'date': datetime.datetime.strptime(response_data['date'], '%Y-%m-%d'),
        'GBP': response_data['rates']['GBP'],
        'USD': response_data['rates']['USD']
    }

    # Create an instance of the model and add it to the session
    currency_rate = CurrencyRate(**data_to_insert)
    session.add(currency_rate)

    start_date += datetime.timedelta(days=1)

# Commit the session to insert the data into the database
session.commit()
