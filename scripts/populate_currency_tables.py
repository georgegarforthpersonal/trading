from sqlalchemy.orm import sessionmaker
from datetime import timedelta, datetime
from constants import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from logger import setup_logger
from src.models import CurrencyRate, CurrencyPair, Base
from src.clients.database import DatabaseConnection
from src.clients.fixer import get_historical

logger = setup_logger(logger_name=__name__)

# Define variables
base_currency = 'EUR'
start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 29)  # Set your end date

# Establish a database connection
db_connection = DatabaseConnection(
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME
)
engine = db_connection.create_engine()

# Create tables if they do not exist
Base.metadata.create_all(engine)

# Populate tables
Session = sessionmaker(bind=engine)
session = Session()
date = start_date
while date <= end_date:
    logger.info(f'Fetching currency data for {date.strftime("%Y-%m-%d")}')
    response_data = get_historical(date.strftime("%Y-%m-%d"), base=base_currency)
    for quote_currency, rate in response_data['rates'].items():
        currency_pair = CurrencyPair.get_or_create(session, base_currency=base_currency, quote_currency=quote_currency)
        currency_rate = CurrencyRate.get_or_create(session, currency_pair_id=currency_pair.id, timestamp=date, rate=rate)
    date += timedelta(days=1)
session.commit()
session.close()
