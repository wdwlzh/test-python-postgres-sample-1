from sqlalchemy import Column, Integer, String, Date, DECIMAL, BIGINT, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import text
from .database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(255))

    prices = relationship("Price", back_populates="stock")
    adjusted_prices = relationship("AdjustedPrice", back_populates="stock")

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(DECIMAL(10, 4))
    high = Column(DECIMAL(10, 4))
    low = Column(DECIMAL(10, 4))
    close = Column(DECIMAL(10, 4))
    volume = Column(BIGINT)

    stock = relationship("Stock", back_populates="prices")

class EMABacktest(Base):
    __tablename__ = "ema_backtests"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    short_period = Column(Integer, nullable=False)
    long_period = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    initial_cash = Column(DECIMAL(15, 2), nullable=False)
    final_cash = Column(DECIMAL(15, 2), nullable=False)
    total_return = Column(DECIMAL(15, 4), nullable=False)
    total_return_percent = Column(DECIMAL(15, 4), nullable=False)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))

class AdjustedPrice(Base):
    __tablename__ = "adjusted_prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    date = Column(Date, nullable=False)
    close = Column(DECIMAL(10, 4))
    high = Column(DECIMAL(10, 4))
    low = Column(DECIMAL(10, 4))
    open = Column(DECIMAL(10, 4))
    volume = Column(BIGINT)
    adj_close = Column(DECIMAL(10, 4))
    adj_high = Column(DECIMAL(10, 4))
    adj_low = Column(DECIMAL(10, 4))
    adj_open = Column(DECIMAL(10, 4))
    adj_volume = Column(BIGINT)
    div_cash = Column(DECIMAL(10, 4))
    split_factor = Column(DECIMAL(10, 4))

    stock = relationship("Stock", back_populates="adjusted_prices")

class Backtest(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    strategy = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    initial_capital = Column(DECIMAL(15, 2))
    final_capital = Column(DECIMAL(15, 2))
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
