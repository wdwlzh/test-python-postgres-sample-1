from . import Strategy
from ..models import Price
from typing import List

class BuyAndHoldStrategy(Strategy):
    def should_buy(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        # Buy on the first day if no position
        return len(prices) == 1 and current_position == 0

    def should_sell(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        # Never sell during the period
        return False
