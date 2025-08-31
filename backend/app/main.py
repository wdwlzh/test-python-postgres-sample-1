from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, get_db
from .models import Base, Stock, Price, Backtest
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import requests
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My FastAPI App", version="1.0.0")

# Pydantic models for API
class StockCreate(BaseModel):
    symbol: str
    name: Optional[str] = None

class StockResponse(StockCreate):
    id: int

class PriceCreate(BaseModel):
    stock_id: int
    date: date
    open_price: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None

class PriceResponse(PriceCreate):
    id: int

class BacktestCreate(BaseModel):
    name: str
    strategy: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    initial_capital: Optional[float] = None
    final_capital: Optional[float] = None

class BacktestResponse(BacktestCreate):
    id: int
    created_at: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI app!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Stock endpoints
@app.post("/stocks/", response_model=StockResponse)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    db_stock = Stock(symbol=stock.symbol, name=stock.name)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@app.get("/stocks/", response_model=List[StockResponse])
def read_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stocks = db.query(Stock).offset(skip).limit(limit).all()
    return stocks

@app.get("/stocks/{stock_id}", response_model=StockResponse)
def read_stock(stock_id: int, db: Session = Depends(get_db)):
    db_stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock

# Price endpoints
@app.post("/prices/", response_model=PriceResponse)
def create_price(price: PriceCreate, db: Session = Depends(get_db)):
    db_price = Price(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

@app.get("/prices/", response_model=List[PriceResponse])
def read_prices(stock_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Price)
    if stock_id:
        query = query.filter(Price.stock_id == stock_id)
    prices = query.offset(skip).limit(limit).all()
    return prices

# Backtest endpoints
@app.post("/backtests/", response_model=BacktestResponse)
def create_backtest(backtest: BacktestCreate, db: Session = Depends(get_db)):
    db_backtest = Backtest(**backtest.dict())
    db.add(db_backtest)
    db.commit()
    db.refresh(db_backtest)
    return db_backtest

@app.get("/backtests/", response_model=List[BacktestResponse])
def read_backtests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    backtests = db.query(Backtest).offset(skip).limit(limit).all()
    return backtests

# Function to fetch data from Alpha Vantage
def fetch_alpha_vantage_data(symbol: str, api_key: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        raise HTTPException(status_code=400, detail=f"Error fetching data: {data.get('Error Message', 'Unknown error')}")
    time_series = data["Time Series (Daily)"]
    prices = []
    for date_str, daily_data in time_series.items():
        price = {
            "date": date_str,
            "open": float(daily_data["1. open"]),
            "high": float(daily_data["2. high"]),
            "low": float(daily_data["3. low"]),
            "close": float(daily_data["4. close"]),
            "volume": int(daily_data["5. volume"])
        }
        prices.append(price)
    return prices

# Endpoint to fetch and store prices
@app.post("/stocks/{symbol}/fetch-prices")
def fetch_and_store_prices(symbol: str, db: Session = Depends(get_db)):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        raise HTTPException(status_code=400, detail="Alpha Vantage API key not set. Please update docker-compose.yml")
    
    # Check if stock exists, if not create
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        stock = Stock(symbol=symbol.upper())
        db.add(stock)
        db.commit()
        db.refresh(stock)
    
    # Fetch data
    prices_data = fetch_alpha_vantage_data(symbol, api_key)
    
    # Insert prices, skip if exists
    inserted_count = 0
    for p in prices_data:
        existing = db.query(Price).filter(Price.stock_id == stock.id, Price.date == p["date"]).first()
        if not existing:
            price = Price(
                stock_id=stock.id,
                date=p["date"],
                open_price=p["open"],
                high=p["high"],
                low=p["low"],
                close=p["close"],
                volume=p["volume"]
            )
            db.add(price)
            inserted_count += 1
    db.commit()
    return {"message": f"Fetched {len(prices_data)} prices, inserted {inserted_count} new records for {symbol}"}
