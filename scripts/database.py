from sqlalchemy.orm import sessionmaker
from datetime import timedelta, datetime

from constants import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from src.models import CurrencyRate, CurrencyPair, Base
from src.clients.database import DatabaseConnection
from src.clients.fixer import get_historical


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

Session = sessionmaker(bind=engine)
session = Session()

base = 'EUR'
start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 28)  # Set your end date

date = start_date

while date <= end_date:

    response_data = get_historical(date.strftime("%Y-%m-%d"), base=base)

    for currency, rate in response_data['rates'].items():

        if currency == base:  # Skip trivial pairs e.g. EUR_EUR
            continue

        # Check if the currency pair already exists in the database
        currency_pair = session.query(CurrencyPair).filter_by(currency_1=base, currency_2=currency).first()
        if not currency_pair:
            # If the currency pair doesn't exist, create a new CurrencyPair instance
            currency_pair = CurrencyPair(id=f'{base}_{currency}', currency_1='EUR', currency_2=currency)
            session.add(currency_pair)

        # Extract data from the API response
        data_to_insert = {
            'id': f'{base}_{currency}_{date.strftime("%Y-%m-%d")}',
            'currency_pair_id': f'{base}_{currency}',
            'timestamp': datetime.strptime(response_data['date'], '%Y-%m-%d'),
            'rate': response_data['rates'][currency]
        }

        # Create an instance of the model and add it to the session
        currency_rate = CurrencyRate(**data_to_insert)
        session.add(currency_rate)

    date += timedelta(days=1)

# Commit the session to insert the data into the database
session.commit()
