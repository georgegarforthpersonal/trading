from sqlalchemy import create_engine, Column, String, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from logger import setup_logger

Base = declarative_base()
logger = setup_logger(logger_name=__name__)


class CurrencyPair(Base):
    __tablename__ = 'currency_pairs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String)
    quote_currency = Column(String)

    # Relationship to CurrencyRate
    currency_rates = relationship("CurrencyRate", back_populates="currency_pair")

    def __str__(self):
        return f"CurrencyPair(id={self.id}, base_currency={self.base_currency}, quote_currency={self.quote_currency})"


    @classmethod
    def get_or_create(cls, session, base_currency: str, quote_currency: str):
        try:
            currency_pair = session.query(cls).filter_by(base_currency=base_currency, quote_currency=quote_currency).one()
            logger.debug(f'Found currency pair {currency_pair}')
        except NoResultFound:
            currency_pair = cls(base_currency=base_currency, quote_currency=quote_currency)
            session.add(currency_pair)
            session.commit()
            logger.debug(f'Created currency pair {currency_pair}')

        return currency_pair


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_pair_id = Column(Integer, ForeignKey('currency_pairs.id'))
    timestamp = Column(DateTime)
    rate = Column(Float)

    # Relationship to CurrencyPair
    currency_pair = relationship("CurrencyPair", back_populates="currency_rates")

    @classmethod
    def get_or_create(cls, session, currency_pair_id, timestamp, rate):
        try:
            currency_rate = session.query(cls).filter_by(currency_pair_id=currency_pair_id, timestamp=timestamp).one()
            logger.debug(f'Found currency rate {currency_rate}')
        except NoResultFound:
            currency_rate = cls(currency_pair_id=currency_pair_id, timestamp=timestamp, rate=rate)
            session.add(currency_rate)
            session.commit()
            logger.debug(f'Created currency rate {currency_rate}')

        return currency_rate

    def __str__(self):
        return f"CurrencyRate(id={self.id}, timestamp={self.timestamp}, rate={self.rate})"
