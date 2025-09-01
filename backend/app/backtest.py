from sqlalchemy.orm import Session
from .models import Stock, Price, Backtest
from .strategies import Strategy
from datetime import date
from typing import List, Dict, Any

class BacktestEngine:
    def __init__(self, strategy: Strategy, symbol: str, start_date: date, end_date: date, initial_cash: float = 10000):
        self.strategy = strategy
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash

    def run(self, db: Session) -> Dict[str, Any]:
        prices = self._get_prices(db)
        if not prices:
            return {"error": "No price data found for the given symbol and date range"}

        cash = self.initial_cash
        position = 0
        trades = []

        for i, price in enumerate(prices):
            current_prices = prices[:i+1]

            if self.strategy.should_buy(current_prices, position, cash):
                if cash > 0:
                    shares = int(cash // float(price.open_price))
                    if shares > 0:
                        cash -= shares * float(price.open_price)
                        position += shares
                        trades.append({
                            'date': price.date.isoformat(),
                            'action': 'buy',
                            'shares': shares,
                            'price': float(price.open_price),
                            'cash_after': cash,
                            'position_after': position
                        })

            if self.strategy.should_sell(current_prices, position, cash):
                if position > 0:
                    cash += position * float(price.close)
                    trades.append({
                        'date': price.date.isoformat(),
                        'action': 'sell',
                        'shares': position,
                        'price': float(price.close),
                        'cash_after': cash,
                        'position_after': 0
                    })
                    position = 0

        # Sell any remaining position at the end
        if position > 0:
            cash += position * float(prices[-1].close)
            trades.append({
                'date': prices[-1].date.isoformat(),
                'action': 'sell',
                'shares': position,
                'price': float(prices[-1].close),
                'cash_after': cash,
                'position_after': 0
            })
            position = 0

        total_value = cash
        total_return = (total_value - self.initial_cash) / self.initial_cash if self.initial_cash > 0 else 0

        return {
            'symbol': self.symbol,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'initial_cash': self.initial_cash,
            'final_cash': total_value,
            'total_return': total_return,
            'total_return_percent': total_return * 100,
            'trades': trades,
            'num_trades': len(trades)
        }

    def _get_prices(self, db: Session) -> List[Price]:
        stock = db.query(Stock).filter(Stock.symbol == self.symbol.upper()).first()
        if not stock:
            return []
        prices = db.query(Price).filter(
            Price.stock_id == stock.id,
            Price.date >= self.start_date,
            Price.date <= self.end_date
        ).order_by(Price.date).all()
        return prices
