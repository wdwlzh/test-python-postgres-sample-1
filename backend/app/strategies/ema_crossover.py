from . import Strategy
from ..models import AdjustedPrice
from typing import List, Optional

class EMACrossoverStrategy(Strategy):
    def __init__(self, short_period: int = 5, long_period: int = 10):
        self.short_period = short_period
        self.long_period = long_period

    def should_buy(self, prices: List[AdjustedPrice], current_position: int, current_cash: float) -> bool:
        if current_position > 0 or len(prices) < self.long_period + 1:
            return False

        ema_short = self._calculate_ema(prices, self.short_period)
        ema_long = self._calculate_ema(prices, self.long_period)

        if ema_short is None or ema_long is None or len(ema_short) < 2 or len(ema_long) < 2:
            return False

        # Check for upward crossover
        if ema_short[-2] <= ema_long[-2] and ema_short[-1] > ema_long[-1]:
            return True
        return False

    def should_sell(self, prices: List[AdjustedPrice], current_position: int, current_cash: float) -> bool:
        if current_position == 0 or len(prices) < self.long_period + 1:
            return False

        ema_short = self._calculate_ema(prices, self.short_period)
        ema_long = self._calculate_ema(prices, self.long_period)

        if ema_short is None or ema_long is None or len(ema_short) < 2 or len(ema_long) < 2:
            return False

        # Check for downward crossover
        if ema_short[-2] >= ema_long[-2] and ema_short[-1] < ema_long[-1]:
            return True
        return False

    def _calculate_ema(self, prices: List[AdjustedPrice], period: int) -> Optional[List[float]]:
        if len(prices) < period:
            return None

        # Use adjusted close prices for EMA calculation
        close_prices = [float(p.adj_close) for p in prices]
        ema = []
        multiplier = 2 / (period + 1)

        # First EMA is SMA
        sma = sum(close_prices[:period]) / period
        ema.append(sma)

        for i in range(period, len(close_prices)):
            ema_val = (close_prices[i] * multiplier) + (ema[-1] * (1 - multiplier))
            ema.append(ema_val)

        return ema
