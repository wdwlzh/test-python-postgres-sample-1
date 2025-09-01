from .models import Price
from typing import List

class Strategy:
    def should_buy(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        """Decide whether to buy based on current data and state."""
        return False

    def should_sell(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        """Decide whether to sell based on current data and state."""
        return False

class BuyAndHoldStrategy(Strategy):
    def should_buy(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        # Buy on the first day if no position
        return len(prices) == 1 and current_position == 0

    def should_sell(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        # Never sell during the period
        return False

# Strategy registry
STRATEGIES = {
    "buy_and_hold": BuyAndHoldStrategy
}
