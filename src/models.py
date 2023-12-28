from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CurrencyPair(Base):
    __tablename__ = 'currency_pairs'

    id = Column(String, primary_key=True)
    currency_1 = Column(String)
    currency_2 = Column(String)

    # Relationship to CurrencyRate
    currency_rates = relationship("CurrencyRate", back_populates="currency_pair")


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(String, primary_key=True)
    currency_pair_id = Column(String, ForeignKey('currency_pairs.id'))
    timestamp = Column(DateTime)
    rate = Column(Float)

    # Relationship to CurrencyPair
    currency_pair = relationship("CurrencyPair", back_populates="currency_rates")
