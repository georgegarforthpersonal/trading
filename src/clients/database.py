from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from constants import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

from src.models import CurrencyPair, CurrencyRate


@dataclass
class DatabaseConnection:
    username: str = DB_USERNAME
    password: str = DB_PASSWORD
    host: str = DB_HOST
    port: int = DB_PORT
    dbname: str = DB_NAME

    def create_engine(self):
        connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        return create_engine(connection_string)

    def get_rates_as_series(
            self,
            base_currency: str,
            quote_currency: str,
            timestamp_after: Optional[datetime] = None,
            timestamp_before: Optional[datetime] = None
    ) -> pd.Series:
        engine = self.create_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            currency_pair = session.query(CurrencyPair).filter_by(base_currency=base_currency,
                                                                  quote_currency=quote_currency).one()
            currency_rates = session.query(CurrencyRate).filter(
                CurrencyRate.currency_pair_id == currency_pair.id)
            if timestamp_after is not None:
                currency_rates = currency_rates.filter(CurrencyRate.timestamp >= timestamp_after)
            if timestamp_before is not None:
                currency_rates = currency_rates.filter(CurrencyRate.timestamp <= timestamp_before)
            rates = [(rate.timestamp, rate.rate) for rate in currency_rates.all()]
            return pd.Series([d[1] for d in rates], index=[d[0] for d in rates]).sort_index()
        except NoResultFound:
            return pd.Series()  # Return an empty series if no results are found
        finally:
            session.close()

